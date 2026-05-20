package pl.staszic.neu.security.repo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import pl.staszic.neu.security.repo.repository.SpringDataUserRepository;
import pl.staszic.neu.security.repo.repository.UserEntity;

import java.util.Optional;

public class DBUserRepository implements UserRepository {

    private static final Logger logger = LoggerFactory.getLogger(DBUserRepository.class);

    private final SpringDataUserRepository jpaRepository;

    public DBUserRepository(SpringDataUserRepository jpaRepository) {
        this.jpaRepository = jpaRepository;
    }

    @Override
    public Optional<StoredUser> findByUsername(String username) {
        return jpaRepository.findByUsername(username).map(entity -> new StoredUser(entity.getUsername(), entity.getPassword()));
    }

    @Override
    public void save(String username, String encodedPassword) {
        if(jpaRepository.findByUsername(username).isPresent()) {
            throw new IllegalArgumentException("Username already exists");
        }
        jpaRepository.save(new UserEntity(username, encodedPassword));
    }
}
