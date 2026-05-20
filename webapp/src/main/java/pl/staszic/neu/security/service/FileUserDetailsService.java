package pl.staszic.neu.security.service;

import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import pl.staszic.neu.security.repo.StoredUser;
import pl.staszic.neu.security.repo.UserRepository;

@Service
public class FileUserDetailsService implements UserDetailsService {

    private final UserRepository userRepository;

    public FileUserDetailsService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        StoredUser user = userRepository
            .findByUsername(username)
            .orElseThrow(() -> new UsernameNotFoundException("Nie znaleziono użytkownika: " + username));

        return User
            .withUsername(user.username())
            .password(user.encodedPassword())
            .roles("USER")
            .build();
    }
}

