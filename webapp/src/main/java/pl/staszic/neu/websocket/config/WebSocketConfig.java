package pl.staszic.neu.websocket.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;
import pl.staszic.neu.websocket.handler.WebSocketHandler;

/**
 * Konfiguracja WebSocket dla aplikacji Spring Boot.
 * Odpowiada za:
 * - rejestrację WebSocket handlera
 * - ustawienie ścieżki, na której będzie dostępny serwer WebSocket
 * - konfigurację dozwolonychorigin (CORS)
 */
@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {
    private final WebSocketHandler webSocketHandler;

    public WebSocketConfig(WebSocketHandler webSocketHandler) {
        this.webSocketHandler = webSocketHandler;
    }

    /**
     * Rejestruje WebSocket handler na określonej ścieżce
     * WebSocket będzie dostępny na: ws://localhost:8080/ws/chat
     * CORS jest domyślnie otwarty (setAllowedOrigins("*"))
     */
    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry
            // Rejestruj handler dla ścieżki "/ws/chat"
            .addHandler(webSocketHandler, "/ws/chat")
            // Zezwól na połączenia z dowolnego origin (CORS)
            .setAllowedOrigins("*");
    }
}


