package pl.staszic.neu.security.repo;

import java.util.Optional;

public interface UserRepository {

    Optional<StoredUser> findByUsername(String username);

    void save(String username, String encodedPassword, Integer matches, Integer wins);

    void save(StoredUser storedUser);

    /**
     * Rejestruje zakończoną grę dla użytkownika: zwiększa licznik rozegranych
     * meczów o 1, a gdy {@code won} jest prawdą, dodatkowo licznik wygranych o 1.
     */
    void recordMatch(String username, boolean won);

}
