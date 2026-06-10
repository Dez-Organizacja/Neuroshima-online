package pl.staszic.neu.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.http.HttpHeaders;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;
import pl.staszic.neu.security.service.TokenAuthService;

import java.io.IOException;
import java.util.Optional;

/**
 * Filtr uwierzytelniający żądania REST na podstawie tokenu Bearer wydanego przez
 * {@link TokenAuthService} (ten sam token, którego używa handshake WebSocket).
 * Dzięki temu chronione endpointy REST są realnie zabezpieczone - bez tokenu
 * SecurityContext pozostaje pusty i reguły z SecurityConfig zwrócą 401.
 */
@Component
public class TokenAuthFilter extends OncePerRequestFilter {

    private static final String BEARER_PREFIX = "Bearer ";

    private final TokenAuthService tokenAuthService;

    public TokenAuthFilter(TokenAuthService tokenAuthService) {
        this.tokenAuthService = tokenAuthService;
    }

    @Override
    protected void doFilterInternal(
        HttpServletRequest request,
        HttpServletResponse response,
        FilterChain filterChain
    ) throws ServletException, IOException {
        String token = extractToken(request);
        if (token != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            Optional<UserDetails> userOpt = tokenAuthService.validate(token);
            userOpt.ifPresent(user -> {
                UsernamePasswordAuthenticationToken auth = new UsernamePasswordAuthenticationToken(
                    user, null, user.getAuthorities()
                );
                SecurityContextHolder.getContext().setAuthentication(auth);
            });
        }
        filterChain.doFilter(request, response);
    }

    private String extractToken(HttpServletRequest request) {
        String header = request.getHeader(HttpHeaders.AUTHORIZATION);
        if (header != null && header.startsWith(BEARER_PREFIX)) {
            return header.substring(BEARER_PREFIX.length()).trim();
        }
        return null;
    }
}
