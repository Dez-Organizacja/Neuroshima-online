package pl.staszic.neu.security.websocket;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpHeaders;
import org.springframework.http.server.ServerHttpRequest;
import org.springframework.http.server.ServletServerHttpRequest;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.server.HandshakeInterceptor;
import pl.staszic.neu.security.service.TokenAuthService;

import java.util.List;
import java.util.Map;
import java.util.Optional;

@Component
public class AuthHandshakeInterceptor implements HandshakeInterceptor {
    private static final Logger logger = LoggerFactory.getLogger(AuthHandshakeInterceptor.class);

    private final TokenAuthService tokenAuthService;

    public AuthHandshakeInterceptor(TokenAuthService tokenAuthService) {
        this.tokenAuthService = tokenAuthService;
    }

    @Override
    public boolean beforeHandshake(
        ServerHttpRequest request,
        org.springframework.http.server.ServerHttpResponse response,
        WebSocketHandler wsHandler,
        Map<String, Object> attributes
    ) {
        String token = extractBearerToken(request);
        if (token == null || token.isBlank()) {
            logger.warn("Brak tokenu podczas handshake WebSocket");
            return false;
        }

        Optional<UserDetails> userOpt = tokenAuthService.validate(token);
        if (userOpt.isEmpty()) {
            logger.warn("Niepoprawny lub wygasły token podczas handshake WebSocket");
            return false;
        }

        attributes.put("authUser", userOpt.get());
        return true;
    }

    @Override
    public void afterHandshake(
        ServerHttpRequest request,
        org.springframework.http.server.ServerHttpResponse response,
        WebSocketHandler wsHandler,
        Exception exception
    ) {
        // no-op
    }

    private String extractBearerToken(ServerHttpRequest request) {
        List<String> values = request.getHeaders().get(HttpHeaders.AUTHORIZATION);
        if (values != null && !values.isEmpty()) {
            for (String value : values) {
                if (value != null && value.startsWith("Bearer ")) {
                    return value.substring("Bearer ".length()).trim();
                }
            }
        }

        if (request instanceof ServletServerHttpRequest servletRequest) {
            String queryToken = servletRequest.getServletRequest().getParameter("token");
            if (queryToken != null && !queryToken.isBlank()) {
                return queryToken.trim();
            }
        }

        return null;
    }
}

