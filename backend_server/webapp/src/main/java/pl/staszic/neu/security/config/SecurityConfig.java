package pl.staszic.neu.security.config;

import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.factory.PasswordEncoderFactories;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import pl.staszic.neu.security.TokenAuthFilter;
import pl.staszic.neu.security.repo.DBUserRepository;
import pl.staszic.neu.security.repo.FileUserRepository;
import pl.staszic.neu.security.repo.UserRepository;
import pl.staszic.neu.security.repo.repository.SpringDataUserRepository;

import java.util.Arrays;
import java.util.List;

@Configuration
public class SecurityConfig {

    @Value("${auth.users.file:users.txt}")
    private String usersFilePath;

    // Lista dozwolonych originów (CORS). Na produkcji ustaw np. https://twoja-domena.
    @Value("${app.cors.allowed-origins:http://localhost:5173,http://localhost:3000,http://localhost:8080}")
    private String allowedOrigins;

    private final TokenAuthFilter tokenAuthFilter;

    public SecurityConfig(TokenAuthFilter tokenAuthFilter) {
        this.tokenAuthFilter = tokenAuthFilter;
    }

    @Bean
    @ConditionalOnProperty(name = "app.user-repository", havingValue = "db", matchIfMissing = true)
    public UserRepository dbUserRepository(SpringDataUserRepository jpaRepo) {
        return new DBUserRepository(jpaRepo);
    }

    @Bean
    @ConditionalOnProperty(name = "app.user-repository", havingValue = "file")
    public UserRepository fileUserRepository() {
        return new FileUserRepository(usersFilePath);
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            // Włączenie obsługi CORS (CorsConfigurationSource bean konfiguruje reguły)
            .cors(Customizer.withDefaults())
            .csrf(csrf -> csrf.disable())
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                // Publiczne: strona powitalna, statyczne zasoby, health i logowanie/rejestracja
                .requestMatchers(
                    "/", "/index.html", "/login.html", "/register.html",
                    "/css/**", "/js/**", "/favicon.ico", "/assets/**",
                    "/api/health", "/api/auth/**"
                ).permitAll()
                // Handshake WebSocket autoryzowany osobno (AuthHandshakeInterceptor)
                .requestMatchers("/ws/**").permitAll()
                // Wszystko inne wymaga ważnego tokenu Bearer
                .anyRequest().authenticated()
            )
            // Token Bearer ustawia uwierzytelnienie przed standardowym filtrem logowania
            .addFilterBefore(tokenAuthFilter, UsernamePasswordAuthenticationFilter.class)
            // Domyślne nagłówki bezpieczeństwa; dodatkowo HSTS gdy ruch idzie przez HTTPS (nginx)
            .headers(headers -> headers
                .frameOptions(frame -> frame.deny())
                .contentTypeOptions(Customizer.withDefaults())
            );

        return http.build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return PasswordEncoderFactories.createDelegatingPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration configuration) throws Exception {
        return configuration.getAuthenticationManager();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(parseOrigins(allowedOrigins));
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        config.setAllowedHeaders(List.of("*"));
        config.setAllowCredentials(true);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }

    public static List<String> parseOrigins(String raw) {
        return Arrays.stream(raw.split(","))
            .map(String::trim)
            .filter(s -> !s.isEmpty())
            .toList();
    }
}
