package pl.staszic.neu.security.repo.repository;

import jakarta.persistence.*;
import org.hibernate.annotations.ColumnDefault;

@Entity
@Table(name = "users")
public class UserEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private String id;

    @Column(unique = true, nullable = false)
    private String username;

    @Column(nullable = false)
    private String password;

    @Column(nullable = false)
    @ColumnDefault("0")
    private Integer matches;

    @Column(nullable = false)
    @ColumnDefault("0")
    private Integer wins;

    public UserEntity() {}

    public UserEntity(String username, String password, Integer matches, Integer wins) {
        this.username = username;
        this.password = password;
        this.matches = matches;
        this.wins = wins;
    }

    public String getUsername() {
        return username;
    }

    public String getPassword() {
        return password;
    }

    public Integer getMatches() {
        return matches;
    }

    public void setMatches(Integer matches) {
        this.matches = matches;
    }

    public Integer getWins() {
        return wins;
    }

    public void setWins(Integer wins) {
        this.wins = wins;
    }
}
