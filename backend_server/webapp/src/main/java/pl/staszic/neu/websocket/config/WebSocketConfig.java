package pl.staszic.neu.websocket.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;
import pl.staszic.neu.security.config.SecurityConfig;
import pl.staszic.neu.security.websocket.AuthHandshakeHandler;
import pl.staszic.neu.security.websocket.AuthHandshakeInterceptor;
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
    private final AuthHandshakeInterceptor authHandshakeInterceptor;
    private final AuthHandshakeHandler authHandshakeHandler;

    // Te same originy co CORS REST; na produkcji ustaw https://twoja-domena.
    @Value("${app.cors.allowed-origins:http://localhost:5173,http://localhost:3000,http://localhost:8080}")
    private String allowedOrigins;

    public WebSocketConfig(
        WebSocketHandler webSocketHandler,
        AuthHandshakeInterceptor authHandshakeInterceptor,
        AuthHandshakeHandler authHandshakeHandler
    ) {
        this.webSocketHandler = webSocketHandler;
        this.authHandshakeInterceptor = authHandshakeInterceptor;
        this.authHandshakeHandler = authHandshakeHandler;
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
            // Dodaj interceptor do autoryzacji handshake
            .addInterceptors(authHandshakeInterceptor)
            // Ustaw handler do obsługi handshake
            .setHandshakeHandler(authHandshakeHandler)
            // Zezwól na połączenia tylko z dozwolonych originów (nie wildcard)
            .setAllowedOrigins(SecurityConfig.parseOrigins(allowedOrigins).toArray(String[]::new));
    }
}
