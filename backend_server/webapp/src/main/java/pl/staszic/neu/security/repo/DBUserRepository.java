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
        return jpaRepository.findByUsername(username).map(entity -> new StoredUser(entity.getUsername(), entity.getPassword(), entity.getMatches(), entity.getWins()));
    }

    @Override
    public void save(String username, String encodedPassword, Integer matches, Integer wins) {
        if(jpaRepository.findByUsername(username).isPresent()) {
            throw new IllegalArgumentException("Username already exists");
        }
        jpaRepository.save(new UserEntity(username, encodedPassword, matches, wins));
    }

    @Override
    public void save(StoredUser storedUser) {
        if(jpaRepository.findByUsername(storedUser.username()).isPresent()) {
            throw new IllegalArgumentException("Username already exists");
        }
        jpaRepository.save(new UserEntity(storedUser.username(), storedUser.encodedPassword(), storedUser.matches(), storedUser.wins()));
    }

    @Override
    public void recordMatch(String username, boolean won) {
        UserEntity entity = jpaRepository.findByUsername(username)
                .orElseThrow(() -> new IllegalArgumentException("Unknown user: " + username));

        entity.setMatches(entity.getMatches() + 1);
        if (won) {
            entity.setWins(entity.getWins() + 1);
        }
        jpaRepository.save(entity);
        logger.info("Recorded match for username={}, won={}, matches={}, wins={}",
                username, won, entity.getMatches(), entity.getWins());
    }
}
