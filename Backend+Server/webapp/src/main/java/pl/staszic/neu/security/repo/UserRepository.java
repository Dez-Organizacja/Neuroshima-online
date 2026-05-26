package pl.staszic.neu.security.repo;

import java.util.Optional;

public interface UserRepository {

    Optional<StoredUser> findByUsername(String username);

    void save(String username, String encodedPassword);



}
