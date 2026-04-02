package pl.staszic.neu.security.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class TokenAuthService {

    private final long tokenTtlSeconds;
    private final Map<String, TokenEntry> tokens = new ConcurrentHashMap<>();

    public TokenAuthService(@Value("${auth.token.ttl-seconds:3600}") long tokenTtlSeconds) {
        this.tokenTtlSeconds = tokenTtlSeconds;
    }

    public TokenIssueResult issueToken(UserDetails user) {
        cleanupExpired();
        String token = UUID.randomUUID().toString().replace("-", "");
        Instant expiresAt = Instant.now().plusSeconds(tokenTtlSeconds);
        tokens.put(token, new TokenEntry(user, expiresAt));
        return new TokenIssueResult(token, expiresAt);
    }

    public Optional<UserDetails> validate(String token) {
        cleanupExpired();
        TokenEntry entry = tokens.get(token);
        if (entry == null || entry.expiresAt().isBefore(Instant.now())) {
            tokens.remove(token);
            return Optional.empty();
        }
        return Optional.of(entry.user());
    }

    private void cleanupExpired() {
        Instant now = Instant.now();
        tokens.entrySet().removeIf(e -> e.getValue().expiresAt().isBefore(now));
    }

    private record TokenEntry(UserDetails user, Instant expiresAt) {
    }

    public record TokenIssueResult(String token, Instant expiresAt) {
    }
}

