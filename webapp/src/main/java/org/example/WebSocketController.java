package org.example;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.HashMap;
import java.util.Map;

/**
 * REST Kontroler do obsługi endpointów WebSocket
 * Dostarcza informacji o stanie połączeń WebSocket
 */
@RestController
public class WebSocketController {

    /**
     * Endpoint zwracający informacje o liczbie aktywnych połączeń WebSocket
     * GET /api/websocket/stats
     * 
     * Zwraca JSON:
     * {
     *   "activeConnections": liczba aktywnych połączeń,
     *   "status": "OK"
     * }
     */
    @GetMapping("/api/websocket/stats")
    public Map<String, Object> getWebSocketStats() {
        Map<String, Object> response = new HashMap<>();
        response.put("activeConnections", WebSocketHandler.getActiveConnectionsCount());
        response.put("status", "OK");
        return response;
    }
}

