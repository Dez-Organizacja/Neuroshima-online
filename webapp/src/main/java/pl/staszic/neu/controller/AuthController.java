package pl.staszic.neu.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import pl.staszic.neu.security.repo.FileUserRepository;
import pl.staszic.neu.security.service.TokenAuthService;

import java.util.Map;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final AuthenticationManager authenticationManager;
    private final TokenAuthService tokenAuthService;
    private final FileUserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public AuthController(
        AuthenticationManager authenticationManager,
        TokenAuthService tokenAuthService,
        FileUserRepository userRepository,
        PasswordEncoder passwordEncoder
    ) {
        this.authenticationManager = authenticationManager;
        this.tokenAuthService = tokenAuthService;
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody AuthRequest request) {
        if (request == null || isBlank(request.username()) || isBlank(request.password())) {
            return ResponseEntity.badRequest().body(Map.of("error", "username i password są wymagane"));
        }

        try {
            userRepository.save(request.username(), passwordEncoder.encode(request.password()));
            return ResponseEntity.status(HttpStatus.CREATED).body(Map.of("status", "registered"));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.status(HttpStatus.CONFLICT).body(Map.of("error", e.getMessage()));
        }
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody AuthRequest request) {
        if (request == null || isBlank(request.username()) || isBlank(request.password())) {
            return ResponseEntity.badRequest().body(Map.of("error", "username i password są wymagane"));
        }

        try {
            Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.username(), request.password())
            );
            UserDetails user = (UserDetails) authentication.getPrincipal();
            TokenAuthService.TokenIssueResult token = tokenAuthService.issueToken(user);
            return ResponseEntity.ok(new AuthResponse(token.token(), token.expiresAt().toString(), user.getUsername()));
        } catch (BadCredentialsException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of("error", "Niepoprawny login lub hasło"));
        }
    }

    private boolean isBlank(String value) {
        return value == null || value.isBlank();
    }

    public record AuthRequest(String username, String password) {
    }

    public record AuthResponse(String token, String expiresAt, String username) {
    }
}

