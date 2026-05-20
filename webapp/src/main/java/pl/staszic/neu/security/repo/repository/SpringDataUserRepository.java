package pl.staszic.neu.security.repo.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface SpringDataUserRepository extends JpaRepository<UserEntity, Long>{
    Optional<UserEntity> findByUsername(String username);
}
