package org.example;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.util.Map;
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
        
        // Utwórz wiadomość JSON o połączeniu
        WebSocketMessage connectionMessage = new WebSocketMessage(
            WebSocketMessage.MessageType.CONNECTION,
            clientId,
            null
        );
        
        // Zloguj informację o połączeniu w formacie JSON
        logger.info("New client connected: {}", objectMapper.writeValueAsString(connectionMessage));
        
        // Wyślij potwierdzenie połączenia do klienta
        String response = objectMapper.writeValueAsString(connectionMessage);
        session.sendMessage(new TextMessage(response));
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
            // Spróbuj sparsować wiadomość jako JSON
            WebSocketMessage incomingMessage = objectMapper.readValue(
                message.getPayload(),
                WebSocketMessage.class
            );
            incomingMessage.setClientId(clientId);
            incomingMessage.setType(WebSocketMessage.MessageType.MESSAGE.getValue());
            
            // Zloguj otrzymaną wiadomość
            logger.info("Message received: {}", objectMapper.writeValueAsString(incomingMessage));
            
            // Utwórz wiadomość echo
            WebSocketMessage echoMessage = new WebSocketMessage(
                WebSocketMessage.MessageType.ECHO,
                clientId,
                incomingMessage.getMessage()
            );
            
            // Zloguj wysyłaną wiadomość echo
            logger.info("Sending echo: {}", objectMapper.writeValueAsString(echoMessage));
            
            // Wyślij echo wiadomość z powrotem do klienta
            String echoResponse = objectMapper.writeValueAsString(echoMessage);
            session.sendMessage(new TextMessage(echoResponse));
            
            // Wyślij wiadomość do wszystkich pozostałych klientów
            broadcastMessage(echoMessage, clientId);
            
        } catch (Exception e) {
            // Jeśli wiadomość nie jest validnym JSON, traktuj ją jako zwykły tekst
            logger.error("Error processing message from client {}: {}", clientId, e.getMessage());
            
            WebSocketMessage errorMessage = new WebSocketMessage(
                WebSocketMessage.MessageType.ECHO,
                clientId,
                message.getPayload()
            );
            
            String response = objectMapper.writeValueAsString(errorMessage);
            session.sendMessage(new TextMessage(response));
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
        
        // Utwórz wiadomość JSON o rozłączeniu
        WebSocketMessage disconnectionMessage = new WebSocketMessage(
            WebSocketMessage.MessageType.DISCONNECTION,
            clientId,
            "Client disconnected with status: " + status.getCode()
        );
        
        // Zloguj informację o rozłączeniu
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
    private void broadcastMessage(WebSocketMessage message, String excludeClientId) {
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
}

