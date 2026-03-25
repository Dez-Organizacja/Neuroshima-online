package pl.staszic.neu;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;

import pl.staszic.neu.messages.EndGameRequest;
import pl.staszic.neu.messages.EndGameResponse;
import pl.staszic.neu.messages.EndTurnRequest;
import pl.staszic.neu.messages.EndTurnResponse;
import pl.staszic.neu.messages.StartNewGameRequest;
import pl.staszic.neu.messages.StartNewGameResponse;
import pl.staszic.neu.messages.WebSocketMessage;

import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Handler dla WebSocket - obsługuje wszystkie zdarzenia WebSocket.
 * Odpowiedzialny za:
 * - obsługę nowych połączeń
 * - wysyłanie echo wiadomości do wszystkich podłączonych klientów
 * - obsługę rozłączania się klientów
 * - logowanie wszystkich połączeń i wiadomości
 */
public class WebSocketHandler extends TextWebSocketHandler {
    private static final Logger logger = LoggerFactory.getLogger(WebSocketHandler.class);
    
    // ObjectMapper do konwersji obiektów Java na JSON i odwrotnie
    private final ObjectMapper objectMapper = new ObjectMapper();
    
    // Mapa przechowująca wszystkie aktywne sesje WebSocket
    // Klucz: unikalny ID klienta, Wartość: sesja WebSocket
    private static final Map<String, WebSocketSession> sessions = new ConcurrentHashMap<>();
    private static final Set<String> activeGames = ConcurrentHashMap.newKeySet();

    /**
     * Metoda wywoływana gdy nowy klient się łączy
     * Generuje unikalny ID dla klienta i loguje połączenie
     */
    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        // Generuj unikalny identyfikator dla każdego klienta
        String clientId = UUID.randomUUID().toString();
        
        // Przechowuj ID klienta w atrybutach sesji
        session.getAttributes().put("clientId", clientId);
        
        // Dodaj sesję do mapy aktywnych sesji
        sessions.put(clientId, session);
        
        Map<String, Object> connectionMessage = new HashMap<>();
        connectionMessage.put("messageType", "CONNECTION");
        connectionMessage.put("clientId", clientId);
        connectionMessage.put("timestamp", LocalDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME));
        connectionMessage.put("message", "Connected");

        logger.info("New client connected: {}", objectMapper.writeValueAsString(connectionMessage));
        session.sendMessage(new TextMessage(objectMapper.writeValueAsString(connectionMessage)));
    }

    /**
     * Metoda wywoływana gdy serwer odbiera wiadomość od klienta
     * Loguje wiadomość i odsyła ją z powrotem (echo)
     */
    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message) throws IOException {
        // Pobierz ID klienta z atrybutów sesji
        String clientId = (String) session.getAttributes().get("clientId");
        
        try {
            JsonNode rootNode = objectMapper.readTree(message.getPayload());
            String messageType = rootNode.path("messageType").asText("").toUpperCase();

            logger.info("Message received from {}: {}", clientId, message.getPayload());

            switch (messageType) {
                case StartNewGameRequest.TYPE -> handleStartNewGame(session, clientId, rootNode);
                case EndGameRequest.TYPE -> handleEndGame(session, clientId, rootNode);
                case EndTurnRequest.TYPE -> handleEndTurn(session, clientId, rootNode);
                default -> sendError(session, clientId, "Unsupported messageType: " + messageType);
            }
            
        } catch (Exception e) {
            // Jeśli wiadomość nie jest validnym JSON, traktuj ją jako zwykły tekst
            logger.error("Error processing message from client {}: {}", clientId, e.getMessage());
            
            sendError(session, clientId, "Invalid payload: " + e.getMessage());
        }
    }

    /**
     * Metoda wywoływana gdy klient się rozłączy
     * Loguje rozłączenie i usuwa sesję z mapy aktywnych sesji
     */
    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        // Pobierz ID klienta
        String clientId = (String) session.getAttributes().get("clientId");
        
        // Usuń sesję z mapy
        sessions.remove(clientId);
        
        Map<String, Object> disconnectionMessage = new HashMap<>();
        disconnectionMessage.put("messageType", "DISCONNECTION");
        disconnectionMessage.put("clientId", clientId);
        disconnectionMessage.put("timestamp", LocalDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME));
        disconnectionMessage.put("message", "Client disconnected with status: " + status.getCode());
        logger.info("Client disconnected: {}", objectMapper.writeValueAsString(disconnectionMessage));
    }

    /**
     * Metoda wywoławana gdy połączenie WebSocket napo tka błąd
     * Loguje błąd i próbuje zamknąć sesję
     */
    @Override
    public void handleTransportError(WebSocketSession session, Throwable exception) throws Exception {
        String clientId = (String) session.getAttributes().get("clientId");
        logger.error("WebSocket error for client {}: {}", clientId, exception.getMessage(), exception);
    }

    /**
     * Wysyła wiadomość do wszystkich podłączonych klientów oprócz wysyłającego
     * @param message wiadomość do wysłania
     * @param excludeClientId ID klienta, który powinien być wyłączony z wysyłania
     */
    private void broadcastMessage(Object message, String excludeClientId) {
        String jsonMessage;
        try {
            jsonMessage = objectMapper.writeValueAsString(message);
        } catch (Exception e) {
            logger.error("Error serializing message for broadcast: {}", e.getMessage());
            return;
        }

        // Iteruj po wszystkich aktywnych sesjach
        sessions.forEach((clientId, session) -> {
            // Wyślij do wszystkich klientów oprócz tego, który wysłał wiadomość
            if (!clientId.equals(excludeClientId) && session.isOpen()) {
                try {
                    session.sendMessage(new TextMessage(jsonMessage));
                } catch (IOException e) {
                    logger.error("Error sending broadcast message to client {}: {}", clientId, e.getMessage());
                }
            }
        });
    }

    /**
     * Zwraca informacje o liczbie aktywnych połączeń
     */
    public static int getActiveConnectionsCount() {
        return sessions.size();
    }

    private void handleStartNewGame(WebSocketSession session, String clientId, JsonNode rootNode) throws IOException {
        StartNewGameRequest request = objectMapper.treeToValue(rootNode, StartNewGameRequest.class);
        request.setClientId(clientId);

        String gameId = UUID.randomUUID().toString();
        activeGames.add(gameId);

        StartNewGameResponse response = new StartNewGameResponse();
        response.setClientId(clientId);
        response.setCreatedGameId(gameId);
        response.setServerStatus("STARTED scenario=" + request.getScenario() + " player=" + request.getPlayerName());

        session.sendMessage(new TextMessage(objectMapper.writeValueAsString(response)));
        logger.info("Game started: {}", objectMapper.writeValueAsString(response));
    }

    private void handleEndGame(WebSocketSession session, String clientId, JsonNode rootNode) throws IOException {
        EndGameRequest request = objectMapper.treeToValue(rootNode, EndGameRequest.class);
        request.setClientId(clientId);

        if (request.getGameId() == null || request.getGameId().isBlank()) {
            sendError(session, clientId, "ENDGAME_REQUEST requires gameId");
            return;
        }
        if (!activeGames.contains(request.getGameId())) {
            sendError(session, clientId, "Unknown gameId: " + request.getGameId());
            return;
        }

        activeGames.remove(request.getGameId());

        EndGameResponse response = new EndGameResponse();
        response.setClientId(clientId);
        response.setGameId(request.getGameId());
        response.setEnded(true);
        response.setSummary("Game ended. Winner=" + request.getWinnerId() + ", reason=" + request.getReason());

        session.sendMessage(new TextMessage(objectMapper.writeValueAsString(response)));
        logger.info("Game ended: {}", objectMapper.writeValueAsString(response));
    }

    private void handleEndTurn(WebSocketSession session, String clientId, JsonNode rootNode) throws IOException {
        EndTurnRequest request = objectMapper.treeToValue(rootNode, EndTurnRequest.class);
        request.setClientId(clientId);

        if (request.getGameId() == null || request.getGameId().isBlank()) {
            sendError(session, clientId, "ENDTURN_REQUEST requires gameId");
            return;
        }
        if (!activeGames.contains(request.getGameId())) {
            sendError(session, clientId, "Unknown gameId: " + request.getGameId());
            return;
        }

        EndTurnResponse response = new EndTurnResponse();
        response.setClientId(clientId);
        response.setGameId(request.getGameId());
        response.setAccepted(true);
        response.setNextPlayerId(request.getPlayerId() + "_next");

        session.sendMessage(new TextMessage(objectMapper.writeValueAsString(response)));
        logger.info("Turn ended: {}", objectMapper.writeValueAsString(response));
        broadcastMessage(response, clientId);
    }

    private void sendError(WebSocketSession session, String clientId, String error) throws IOException {
        Map<String, Object> errorMessage = new HashMap<>();
        errorMessage.put("messageType", "ERROR");
        errorMessage.put("timestamp", LocalDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME));
        errorMessage.put("clientId", clientId);
        errorMessage.put("error", error);
        session.sendMessage(new TextMessage(objectMapper.writeValueAsString(errorMessage)));
    }
}

