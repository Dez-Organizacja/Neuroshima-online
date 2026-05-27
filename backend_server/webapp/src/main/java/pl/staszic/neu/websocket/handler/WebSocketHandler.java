package pl.staszic.neu.websocket.handler;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;
import pl.staszic.neu.game.service.GameService;
import pl.staszic.neu.game.service.GameValidationException;
import pl.staszic.neu.messages.*;
import pl.staszic.neu.websocket.session.WebSocketSessionRegistry;

import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;

@Component
public class WebSocketHandler extends TextWebSocketHandler {
    private static final Logger logger = LoggerFactory.getLogger(WebSocketHandler.class);

    private final ObjectMapper objectMapper;
    private final GameService gameService;
    private final WebSocketSessionRegistry sessionRegistry;

    public WebSocketHandler(
            ObjectMapper objectMapper,
            GameService gameService,
            WebSocketSessionRegistry sessionRegistry
    ) {
        this.objectMapper = objectMapper;
        this.gameService = gameService;
        this.sessionRegistry = sessionRegistry;
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        UserDetails user = getAuthenticatedUser(session);
        if (user == null) {
            logger.warn("Brak authUser w sesji WebSocket - zamykam połączenie");
            session.close(CloseStatus.POLICY_VIOLATION);
            return;
        }

        // Tłumaczymy techniczną sesję na konkretnego użytkownika
        String sessionId = session.getId();
        String username = user.getUsername();

        session.getAttributes().put("clientId", sessionId);
        session.getAttributes().put("username", username);

        sessionRegistry.register(sessionId, session);
        gameService.registerClientUsername(sessionId, username); // ← Przekazujemy username do serwisu gry

        Map<String, Object> connectionMessage = new HashMap<>();
        connectionMessage.put("messageType", "CONNECTION");
        connectionMessage.put("clientId", sessionId);
        connectionMessage.put("username", username);
        connectionMessage.put("timestamp", LocalDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME));
        connectionMessage.put("message", "Connected");

        logger.info("Authenticated client {} connected as session: {}", username, sessionId);
        sendJson(session, connectionMessage);
    }

    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message) throws IOException {
        String clientId = (String) session.getAttributes().get("clientId");

        try {
            UserDetails user = getAuthenticatedUser(session);
            if (user == null) {
                sendError(session, clientId, "Unauthorized session");
                session.close(CloseStatus.POLICY_VIOLATION);
                return;
            }

            JsonNode rootNode = objectMapper.readTree(message.getPayload());
            String messageType = rootNode.path("messageType").asText("").toUpperCase();
            logger.info("Message received from {}: {}", user.getUsername(), message.getPayload());

            switch (messageType) {
                case GetRoomStatusRequest.TYPE -> handleGetRoomStatus(session, clientId, rootNode);
                case SetFactionRequest.TYPE -> handleSetFaction(session, clientId, rootNode);
                case ActionRequest.TYPE -> handleActionRequest(clientId, rootNode);
                case JoinRoomRequest.TYPE -> handleJoinRoom(session, clientId, rootNode);
                case LeaveRoomRequest.TYPE -> handleLeaveRoom(session, clientId, rootNode);
                case CreateNewRoomRequest.TYPE -> handleCreateNewRoom(session, clientId, rootNode);
                case NewGameRequest.TYPE -> handleStartNewGame(session, clientId, rootNode);
                case EndGameRequest.TYPE -> handleEndGame(session, clientId, rootNode);
                default -> sendError(session, clientId, "Unsupported messageType: " + messageType);
            }
        } catch (GameValidationException e) {
            sendError(session, clientId, e.getMessage());
        } catch (Exception e) {
            logger.error("Error processing message from client {}: {}", clientId, e.getMessage());
            sendError(session, clientId, "Invalid payload: " + e.getMessage());
        }
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        String clientId = (String) session.getAttributes().get("clientId");
        String roomId = gameService.getAffiliation(clientId);
        sessionRegistry.unregister(clientId);
        gameService.handleClientDisconnect(clientId);
        broadcastRoomStatus(roomId);

        Map<String, Object> disconnectionMessage = new HashMap<>();
        disconnectionMessage.put("messageType", "DISCONNECTION");
        disconnectionMessage.put("clientId", clientId);
        disconnectionMessage.put("timestamp", LocalDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME));
        disconnectionMessage.put("message", "Client disconnected with status: " + status.getCode());
        logger.info("Client disconnected: {}", objectMapper.writeValueAsString(disconnectionMessage));
    }

    @Override
    public void handleTransportError(WebSocketSession session, Throwable exception) {
        String clientId = (String) session.getAttributes().get("clientId");
        logger.error("WebSocket error for client {}: {}", clientId, exception.getMessage(), exception);
    }

    private void handleCreateNewRoom(WebSocketSession session, String clientId, JsonNode rootNode) throws IOException {
        CreateNewRoomRequest request = objectMapper.treeToValue(rootNode, CreateNewRoomRequest.class);
        CreateNewRoomResponse response = gameService.createNewRoom(clientId, request);
        sendJson(session, response);
        broadcastRoomStatus(request.getRoomId());
        logger.info("Room created: {}", objectMapper.writeValueAsString(response));
    }

    private void handleJoinRoom(WebSocketSession session, String clientId, JsonNode rootNode) throws IOException {
        JoinRoomRequest request = objectMapper.treeToValue(rootNode, JoinRoomRequest.class);
        JoinRoomResponse response = gameService.joinRoom(clientId, request);
        sendJson(session, response);
        broadcastRoomStatus(request.getRoomId());
        logger.info("Room joined: {}", objectMapper.writeValueAsString(response));
    }

    private void handleLeaveRoom(WebSocketSession session, String clientId, JsonNode rootNode) throws IOException {
        LeaveRoomRequest request = objectMapper.treeToValue(rootNode, LeaveRoomRequest.class);
        String roomId = request.getRoomId();
        LeaveRoomResponse response = gameService.leaveRoom(clientId, request);
        sendJson(session, response);
        broadcastRoomStatus(roomId);
        logger.info("Room left: {}", objectMapper.writeValueAsString(response));
    }

    private void handleGetRoomStatus(WebSocketSession session, String clientId, JsonNode rootNode) throws IOException {
        GetRoomStatusRequest request = objectMapper.treeToValue(rootNode, GetRoomStatusRequest.class);
        GetRoomStatusResponse response = gameService.getRoomStatus(clientId, request);
        sendJson(session, response);
        logger.info("Room status: {}", objectMapper.writeValueAsString(response));
    }

    private void handleSetFaction(WebSocketSession session, String clientId, JsonNode rootNode) throws IOException {
        SetFactionRequest request = objectMapper.treeToValue(rootNode, SetFactionRequest.class);
        SetFactionResponse response = gameService.setFaction(clientId, request);
        sendJson(session, response);

        String roomId = gameService.getAffiliation(clientId);
        if (response.getError() == null && roomId != null) {
            broadcastRoomStatus(roomId);
        }

        logger.info("Faction selected: {}", objectMapper.writeValueAsString(response));
    }

    private void handleStartNewGame(WebSocketSession session, String clientId, JsonNode rootNode) throws IOException {
        NewGameRequest request = objectMapper.treeToValue(rootNode, NewGameRequest.class);
        NewGameResponse response = gameService.startNewGame(clientId, request);

        broadcastToRoom(response, response.getRoomId());
        logger.info("Game started: {}", objectMapper.writeValueAsString(response));
    }

    private void handleActionRequest(String clientId, JsonNode rootNode) throws IOException {
        ActionRequest request = objectMapper.treeToValue(rootNode, ActionRequest.class);
        ActionResponse response = gameService.processAction(clientId, request);

        String roomId = gameService.getAffiliation(clientId);
        broadcastToRoom(response, roomId);

        logger.info("Action processed for client {}", clientId);
    }
    
    private void handleEndGame(WebSocketSession session, String clientId, JsonNode rootNode) throws IOException {
        EndGameRequest request = objectMapper.treeToValue(rootNode, EndGameRequest.class);
        EndGameResponse response = gameService.endGame(clientId, request);
        sendJson(session, response);
        logger.info("Game ended: {}", objectMapper.writeValueAsString(response));
    }

    private void broadcastMessage(Object message, String excludeRoomId) {
        String jsonMessage;
        try {
            jsonMessage = objectMapper.writeValueAsString(message);
        } catch (Exception e) {
            logger.error("Error serializing message for broadcast: {}", e.getMessage());
            return;
        }

        sessionRegistry.getSessions().forEach((roomId, session) -> {
            if (!message.equals(excludeRoomId) && session.isOpen()) {
                try {
                    session.sendMessage(new TextMessage(jsonMessage));
                } catch (IOException e) {
                    logger.error("Error sending broadcast message to client {}: {}", excludeRoomId, e.getMessage());
                }
            }
        });
    }

    private void sendJson(WebSocketSession session, Object payload) throws IOException {
        session.sendMessage(new TextMessage(objectMapper.writeValueAsString(payload)));
    }

    private void broadcastRoomStatus(String roomId) {
        if (roomId == null || roomId.isBlank()) {
            return;
        }

        for (String targetClientId : gameService.getClientIdsInRoom(roomId)) {
            WebSocketSession targetSession = sessionRegistry.getSessions().get(targetClientId);

            if (targetSession == null || !targetSession.isOpen()) {
                continue;
            }

            try {
                GetRoomStatusRequest statusRequest = new GetRoomStatusRequest();
                statusRequest.setRoomId(roomId);

                GetRoomStatusResponse statusResponse = gameService.getRoomStatus(targetClientId, statusRequest);
                sendJson(targetSession, statusResponse);
            } catch (GameValidationException e) {
                logger.warn(
                    "Could not send room status to client {} in room {}: {}",
                    targetClientId,
                    roomId,
                    e.getMessage()
                );
            } catch (IOException e) {
                logger.error(
                    "Error sending room status to client {} in room {}: {}",
                    targetClientId,
                    roomId,
                    e.getMessage()
                );
            }
        }
    }

    private void broadcastToRoom(Object payload, String roomId) {
        String jsonMessage;

        try {
            jsonMessage = objectMapper.writeValueAsString(payload);
        } catch (Exception e) {
            logger.error("Error serializing message for room broadcast: {}", e.getMessage());
            return;
        }

        for (String targetClientId : gameService.getClientIdsInRoom(roomId)) {
            WebSocketSession targetSession = sessionRegistry.getSessions().get(targetClientId);

            if (targetSession == null || !targetSession.isOpen()) {
                continue;
            }

            try {
                targetSession.sendMessage(new TextMessage(jsonMessage));
            } catch (IOException e) {
                logger.error(
                    "Error sending message to client {} in room {}: {}",
                    targetClientId,
                    roomId,
                    e.getMessage()
                );
            }
        }
    }

    private void sendError(WebSocketSession session, String clientId, String error) throws IOException {
        Map<String, Object> errorMessage = new HashMap<>();
        errorMessage.put("messageType", "ERROR");
        errorMessage.put("timestamp", LocalDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME));
        errorMessage.put("clientId", clientId);
        errorMessage.put("error", error);
        sendJson(session, errorMessage);
    }

    private UserDetails getAuthenticatedUser(WebSocketSession session) {
        Object authUser = session.getAttributes().get("authUser");
        if (authUser instanceof UserDetails userDetails) {
            return userDetails;
        }
        return null;
    }
}
