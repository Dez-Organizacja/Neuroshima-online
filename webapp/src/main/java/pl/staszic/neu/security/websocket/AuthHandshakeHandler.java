
package pl.staszic.neu.security.websocket;

import org.springframework.http.server.ServerHttpRequest;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.server.support.DefaultHandshakeHandler;

import java.security.Principal;
import java.util.Map;

@Component
public class AuthHandshakeHandler extends DefaultHandshakeHandler {

    @Override
    protected Principal determineUser(
        ServerHttpRequest request,
        WebSocketHandler wsHandler,
        Map<String, Object> attributes
    ) {
        Object authUser = attributes.get("authUser");
        if (authUser instanceof UserDetails userDetails) {
            return userDetails::getUsername;
        }
        return super.determineUser(request, wsHandler, attributes);
    }
}

