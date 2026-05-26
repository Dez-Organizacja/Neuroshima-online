package pl.staszic.neu.websocket.session;

import org.springframework.stereotype.Component;
import org.springframework.web.socket.WebSocketSession;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Component
public class WebSocketSessionRegistry {
    private final Map<String, WebSocketSession> sessions = new ConcurrentHashMap<>();

    public void register(String clientId, WebSocketSession session) {
        sessions.put(clientId, session);
    }

    public void unregister(String clientId) {
        sessions.remove(clientId);
    }

    public int getActiveConnectionsCount() {
        return sessions.size();
    }

    public Map<String, WebSocketSession> getSessions() {
        return sessions;
    }
}

