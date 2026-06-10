package pl.staszic.neu.security.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.imageio.ImageIO;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.geom.AffineTransform;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.security.SecureRandom;
import java.time.Instant;
import java.util.Base64;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Captcha obrazkowa generowana po stronie serwera (challenge/response), self-hosted.
 *
 * Działa dla DOWOLNEGO klienta (przeglądarka, aplikacja Python, curl) - inaczej niż
 * Cloudflare Turnstile, który wymaga widgetu JS w przeglądarce.
 *
 * Przepływ:
 *   1. klient woła issue() (GET /api/auth/captcha) -> dostaje captchaId + obraz PNG,
 *   2. użytkownik przepisuje kod z obrazka,
 *   3. klient wysyła captchaId + odpowiedź do rejestracji, serwer woła verify().
 *
 * Wyzwanie jest JEDNORAZOWE (konsumowane przy verify) i ma ograniczony czas życia (TTL).
 *
 * Flaga 'captcha.required' (domyślnie false) decyduje, czy rejestracja WYMAGA captchy:
 *   - false (domyślnie): verify() zawsze zwraca true -> rejestracja bez captchy (wstecznie
 *     kompatybilne). Endpoint /api/auth/captcha działa mimo to, więc klient może dorabiać obsługę.
 *   - true: rejestracja wymaga poprawnego, niewygasłego wyzwania.
 */
@Service
public class CaptchaService {

    // Alfabet bez znaków łatwych do pomylenia (brak 0/O, 1/I/L).
    private static final char[] ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789".toCharArray();
    private static final int WIDTH = 170;
    private static final int HEIGHT = 60;

    private final boolean required;
    private final int codeLength;
    private final long ttlSeconds;
    private final SecureRandom random = new SecureRandom();
    private final Map<String, Challenge> challenges = new ConcurrentHashMap<>();

    public CaptchaService(
        @Value("${captcha.required:false}") boolean required,
        @Value("${captcha.length:5}") int codeLength,
        @Value("${captcha.ttl-seconds:300}") long ttlSeconds
    ) {
        this.required = required;
        this.codeLength = codeLength;
        this.ttlSeconds = ttlSeconds;
    }

    /** Czy rejestracja wymaga poprawnej captchy. */
    public boolean isRequired() {
        return required;
    }

    /**
     * Wystawia nowe wyzwanie: losowy kod zapisany w pamięci (z TTL) + jego obraz jako data URI PNG.
     */
    public IssuedCaptcha issue() {
        cleanupExpired();
        String code = randomCode();
        String captchaId = UUID.randomUUID().toString().replace("-", "");
        challenges.put(captchaId, new Challenge(code, Instant.now().plusSeconds(ttlSeconds)));
        String image = "data:image/png;base64," + Base64.getEncoder().encodeToString(renderPng(code));
        return new IssuedCaptcha(captchaId, image);
    }

    /**
     * Weryfikuje odpowiedź na wyzwanie. Wyzwanie jest konsumowane (usuwane) niezależnie od wyniku,
     * więc jednego captchaId nie da się użyć ponownie ani zgadywać metodą prób.
     *
     * @return true gdy captcha nie jest wymagana albo gdy wyzwanie istnieje, nie wygasło i kod się zgadza.
     */
    public boolean verify(String captchaId, String answer) {
        if (!required) {
            return true;
        }
        if (captchaId == null || answer == null || answer.isBlank()) {
            return false;
        }
        cleanupExpired();
        Challenge challenge = challenges.remove(captchaId); // jednorazowa konsumpcja
        if (challenge == null || challenge.expiresAt().isBefore(Instant.now())) {
            return false;
        }
        return challenge.code().equalsIgnoreCase(answer.trim());
    }

    private String randomCode() {
        StringBuilder sb = new StringBuilder(codeLength);
        for (int i = 0; i < codeLength; i++) {
            sb.append(ALPHABET[random.nextInt(ALPHABET.length)]);
        }
        return sb.toString();
    }

    private byte[] renderPng(String code) {
        BufferedImage img = new BufferedImage(WIDTH, HEIGHT, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = img.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        // Tło
        g.setColor(new Color(238, 240, 245));
        g.fillRect(0, 0, WIDTH, HEIGHT);

        // Szum: losowe linie utrudniające OCR
        for (int i = 0; i < 7; i++) {
            g.setColor(new Color(random.nextInt(200), random.nextInt(200), random.nextInt(200)));
            g.drawLine(random.nextInt(WIDTH), random.nextInt(HEIGHT), random.nextInt(WIDTH), random.nextInt(HEIGHT));
        }

        // Znaki - każdy z lekkim, losowym obrotem i kolorem
        int x = 14;
        for (char c : code.toCharArray()) {
            int fontSize = 30 + random.nextInt(8);
            g.setFont(new Font("SansSerif", Font.BOLD, fontSize));
            g.setColor(new Color(random.nextInt(120), random.nextInt(120), random.nextInt(120)));
            int y = 38 + random.nextInt(10);
            double angle = (random.nextDouble() - 0.5) * 0.6; // ok. ±17 stopni
            AffineTransform original = g.getTransform();
            g.rotate(angle, x, y);
            g.drawString(String.valueOf(c), x, y);
            g.setTransform(original);
            x += 26 + random.nextInt(6);
        }

        // Szum: losowe kropki
        for (int i = 0; i < 140; i++) {
            img.setRGB(random.nextInt(WIDTH), random.nextInt(HEIGHT), random.nextInt(0xFFFFFF));
        }

        g.dispose();
        try {
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            ImageIO.write(img, "png", out);
            return out.toByteArray();
        } catch (IOException e) {
            throw new UncheckedIOException("Nie udało się wygenerować obrazu CAPTCHA", e);
        }
    }

    private void cleanupExpired() {
        Instant now = Instant.now();
        challenges.entrySet().removeIf(e -> e.getValue().expiresAt().isBefore(now));
    }

    private record Challenge(String code, Instant expiresAt) {
    }

    /** Wystawione wyzwanie zwracane do klienta. {@code image} to data URI PNG (base64). */
    public record IssuedCaptcha(String captchaId, String image) {
    }
}
