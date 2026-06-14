package pl.staszic.neu.security.repo;

public record StoredUser(String username, String encodedPassword, Integer matches, Integer wins) {
}
