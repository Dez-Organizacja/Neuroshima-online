package pl.staszic.neu.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * Publiczny endpoint statusu usługi (używany przez stronę powitalną i monitoring).
 */
@RestController
public class Controller {

    @GetMapping("/api/health")
    public Map<String, String> health() {
        return Map.of("status", "UP");
    }
}
