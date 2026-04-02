package pl.staszic.neu.security.repo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Repository;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.List;
import java.util.Optional;

@Repository
public class FileUserRepository {
    private static final Logger logger = LoggerFactory.getLogger(FileUserRepository.class);

    private final Path usersFile;

    public FileUserRepository(@Value("${auth.users.file:users.txt}") String usersFilePath) {
        this.usersFile = Path.of(usersFilePath);
        ensureFileExists();
    }

    public Optional<StoredUser> findByUsername(String username) {
        try {
            List<String> lines = Files.readAllLines(usersFile, StandardCharsets.UTF_8);
            for (String rawLine : lines) {
                StoredUser parsed = parseLine(rawLine);
                if (parsed != null && parsed.username().equals(username)) {
                    return Optional.of(parsed);
                }
            }
            return Optional.empty();
        } catch (IOException e) {
            throw new IllegalStateException("Nie można odczytać pliku użytkowników: " + usersFile, e);
        }
    }

    public synchronized void save(String username, String encodedPassword) {
        if (findByUsername(username).isPresent()) {
            throw new IllegalArgumentException("Użytkownik już istnieje: " + username);
        }

        String line = username + ":" + encodedPassword + System.lineSeparator();
        try {
            Files.writeString(usersFile, line, StandardCharsets.UTF_8, StandardOpenOption.APPEND);
        } catch (IOException e) {
            throw new IllegalStateException("Nie można zapisać użytkownika do pliku: " + usersFile, e);
        }
    }

    private StoredUser parseLine(String rawLine) {
        String line = rawLine == null ? "" : rawLine.trim();
        if (line.isEmpty() || line.startsWith("#")) {
            return null;
        }

        if (line.startsWith("Username:") && line.contains(", Password:")) {
            String withoutPrefix = line.substring("Username:".length()).trim();
            String[] parts = withoutPrefix.split(", Password:", 2);
            if (parts.length == 2) {
                return new StoredUser(parts[0].trim(), "{noop}" + parts[1].trim());
            }
            return null;
        }

        int separatorIdx = line.indexOf(':');
        if (separatorIdx <= 0 || separatorIdx >= line.length() - 1) {
            return null;
        }

        String username = line.substring(0, separatorIdx).trim();
        String password = line.substring(separatorIdx + 1).trim();
        if (password.startsWith("{")) {
            return new StoredUser(username, password);
        }
        if (password.startsWith("$2a$") || password.startsWith("$2b$") || password.startsWith("$2y$")) {
            return new StoredUser(username, "{bcrypt}" + password);
        }
        return new StoredUser(username, "{noop}" + password);
    }

    private void ensureFileExists() {
        try {
            Path parent = usersFile.getParent();
            if (parent != null) {
                Files.createDirectories(parent);
            }
            if (!Files.exists(usersFile)) {
                Files.createFile(usersFile);
                logger.info("Utworzono plik użytkowników: {}", usersFile.toAbsolutePath());
            }
        } catch (IOException e) {
            throw new IllegalStateException("Nie można utworzyć pliku użytkowników: " + usersFile, e);
        }
    }

    public record StoredUser(String username, String encodedPassword) {
    }
}

