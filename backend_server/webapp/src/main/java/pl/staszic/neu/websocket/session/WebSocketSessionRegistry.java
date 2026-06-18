package pl.staszic.neu.websocket.session;

import org.springframework.stereotype.Component;
import org.springframework.web.socket.WebSocketSession;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Component
public class WebSocketSessionRegistry {
    private final Map<String, WebSocketSession> sessions = new ConcurrentHashMap<>();

    /**
     * Registers the current socket for a stable player id and returns the
     * previously registered socket, if one existed.
     */
    public WebSocketSession register(String clientId, WebSocketSession session) {
        return sessions.put(clientId, session);
    }

    /**
     * Removes the mapping only when it still points at this exact socket.
     * This prevents an old socket closing during a refresh from unregistering
     * the replacement socket that has already connected.
     */
    public boolean unregister(String clientId, WebSocketSession session) {
        return sessions.remove(clientId, session);
    }

    public int getActiveConnectionsCount() {
        return sessions.size();
    }

    public Map<String, WebSocketSession> getSessions() {
        return sessions;
    }
}
