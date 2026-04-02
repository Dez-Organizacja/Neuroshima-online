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

        String clientId = user.getUsername();
        session.getAttributes().put("clientId", clientId);
        sessionRegistry.register(clientId, session);

        Map<String, Object> connectionMessage = new HashMap<>();
        connectionMessage.put("messageType", "CONNECTION");
        connectionMessage.put("clientId", clientId);
        connectionMessage.put("username", user.getUsername());
        connectionMessage.put("timestamp", LocalDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME));
        connectionMessage.put("message", "Connected");

        logger.info("Authenticated client connected: {}", objectMapper.writeValueAsString(connectionMessage));
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
        sessionRegistry.unregister(clientId);
        gameService.handleClientDisconnect(clientId);

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
        logger.info("Room created: {}", objectMapper.writeValueAsString(response));
    }

    private void handleJoinRoom(WebSocketSession session, String clientId, JsonNode rootNode) throws IOException {
        JoinRoomRequest request = objectMapper.treeToValue(rootNode, JoinRoomRequest.class);
        JoinRoomResponse response = gameService.joinRoom(clientId, request);
        sendJson(session, response);
        logger.info("Room joined: {}", objectMapper.writeValueAsString(response));
    }

    private void handleLeaveRoom(WebSocketSession session, String clientId, JsonNode rootNode) throws IOException {
        LeaveRoomRequest request = objectMapper.treeToValue(rootNode, LeaveRoomRequest.class);
        LeaveRoomResponse response = gameService.leaveRoom(clientId, request);
        sendJson(session, response);
        logger.info("Room left: {}", objectMapper.writeValueAsString(response));
    }

    private void handleGetRoomStatus(WebSocketSession session, String clientId, JsonNode rootNode) throws IOException {
        GetRoomStatusRequest request = objectMapper.treeToValue(rootNode, GetRoomStatusRequest.class);
        GetRoomStatusResponse response = gameService.getRoomStatus(clientId, request);
        sendJson(session, response);
        logger.info("Room status: {}", objectMapper.writeValueAsString(response));
    }

    private void handleStartNewGame(WebSocketSession session, String clientId, JsonNode rootNode) throws IOException {
        NewGameRequest request = objectMapper.treeToValue(rootNode, NewGameRequest.class);
        NewGameResponse response = gameService.startNewGame(clientId, request);
        sendJson(session, response);
        logger.info("Game started: {}", objectMapper.writeValueAsString(response));
    }

    private void handleActionRequest(String clientId, JsonNode rootNode) throws IOException {
        ActionRequest request = objectMapper.treeToValue(rootNode, ActionRequest.class);
        gameService.processAction(clientId, request);
        logger.info("Action processed for client {}", clientId);
    }

    private void handleEndGame(WebSocketSession session, String clientId, JsonNode rootNode) throws IOException {
        EndGameRequest request = objectMapper.treeToValue(rootNode, EndGameRequest.class);
        EndGameResponse response = gameService.endGame(clientId, request);
        sendJson(session, response);
        logger.info("Game ended: {}", objectMapper.writeValueAsString(response));
    }

    private void broadcastMessage(Object message, String excludeClientId) {
        String jsonMessage;
        try {
            jsonMessage = objectMapper.writeValueAsString(message);
        } catch (Exception e) {
            logger.error("Error serializing message for broadcast: {}", e.getMessage());
            return;
        }

        sessionRegistry.getSessions().forEach((clientId, session) -> {
            if (!clientId.equals(excludeClientId) && session.isOpen()) {
                try {
                    session.sendMessage(new TextMessage(jsonMessage));
                } catch (IOException e) {
                    logger.error("Error sending broadcast message to client {}: {}", clientId, e.getMessage());
                }
            }
        });
    }

    private void sendJson(WebSocketSession session, Object payload) throws IOException {
        session.sendMessage(new TextMessage(objectMapper.writeValueAsString(payload)));
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
