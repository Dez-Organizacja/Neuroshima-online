package pl.staszic.neu.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import pl.staszic.neu.security.repo.UserRepository;
import pl.staszic.neu.security.service.CaptchaService;
import pl.staszic.neu.security.service.TokenAuthService;

import java.util.Map;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final AuthenticationManager authenticationManager;
    private final TokenAuthService tokenAuthService;
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final CaptchaService captchaService;

    // Czy rejestracja przez API jest dostępna. Domyślnie true (odblokowana).
    // Na produkcji ustaw auth.registration.enabled=false aby zablokować.
    @Value("${auth.registration.enabled:true}")
    private boolean registrationEnabled;

    public AuthController(
        AuthenticationManager authenticationManager,
        TokenAuthService tokenAuthService,
        UserRepository userRepository,
        PasswordEncoder passwordEncoder,
        CaptchaService captchaService
    ) {
        this.authenticationManager = authenticationManager;
        this.tokenAuthService = tokenAuthService;
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.captchaService = captchaService;
    }

    /**
     * Konfiguracja rejestracji dla frontu (czy włączona + czy wymagana captcha).
     */
    @GetMapping("/registration-config")
    public Map<String, Object> registrationConfig() {
        return Map.of(
            "registrationEnabled", registrationEnabled,
            "captchaRequired", captchaService.isRequired()
        );
    }

    /**
     * Wystawia nowe wyzwanie CAPTCHA (obrazek + identyfikator).
     * Klient pokazuje obraz, użytkownik przepisuje kod, a klient odsyła captchaId + captchaAnswer
     * w żądaniu rejestracji. Wyzwanie jest jednorazowe i wygasa po krótkim czasie (TTL).
     */
    @GetMapping("/captcha")
    public ResponseEntity<?> captcha() {
        if (!registrationEnabled) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN).body(Map.of("error", "registration disabled"));
        }
        CaptchaService.IssuedCaptcha challenge = captchaService.issue();
        return ResponseEntity.ok(Map.of(
            "captchaId", challenge.captchaId(),
            "image", challenge.image()
        ));
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody AuthRequest request) {
        if (!registrationEnabled) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN).body(Map.of("error", "registration disabled"));
        }
        if (request == null || isBlank(request.username()) || isBlank(request.password())) {
            return ResponseEntity.badRequest().body(Map.of("error", "username i password są wymagane"));
        }
        if (!captchaService.verify(request.captchaId(), request.captchaAnswer())) {
            return ResponseEntity.badRequest().body(Map.of("error", "Weryfikacja CAPTCHA nieudana"));
        }

        try {
            userRepository.save(request.username(), passwordEncoder.encode(request.password()), 0, 0);
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

    public record AuthRequest(String username, String password, String captchaId, String captchaAnswer) {
    }

    public record AuthResponse(String token, String expiresAt, String username) {
    }
}

