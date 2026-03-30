package pl.staszic.neu.rest.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;
import java.util.List;

@Service
public class InMemoryRestService implements RestService {
    private static final Logger logger = LoggerFactory.getLogger(InMemoryRestService.class);

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    @Autowired
    public InMemoryRestService(RestTemplateBuilder restTemplateBuilder, ObjectMapper objectMapper) {
        this.restTemplate = restTemplateBuilder.build();
        this.objectMapper = objectMapper;
    }

    @Override
    public JsonNode postJson(String url, JsonNode requestBody) {
        if (url == null || url.isBlank()) {
            throw new IllegalArgumentException("URL nie może być pusty");
        }
        if (requestBody == null || requestBody.isNull()) {
            throw new IllegalArgumentException("Request body nie może być pusty");
        }

        try {
            logger.info("Wysyłam POST request na: {}", url);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.setAccept(List.of(MediaType.APPLICATION_JSON, MediaType.TEXT_HTML, MediaType.ALL));

            HttpEntity<String> entity = new HttpEntity<>(requestBody.toString(), headers);
            ResponseEntity<String> responseEntity = restTemplate.postForEntity(url, entity, String.class);
            String body = responseEntity.getBody();

            if (body == null || body.isBlank()) {
                logger.warn("Odpowiedź z {} jest pusta", url);
                throw new RuntimeException("Serwer zwrócił pustą odpowiedź");
            }

            JsonNode response = objectMapper.readTree(body);
            logger.info("Otrzymano odpowiedź z: {}", url);
            return response;
        } catch (IOException e) {
            logger.error("Odpowiedź z {} nie jest poprawnym JSON-em: {}", url, e.getMessage());
            throw new RuntimeException("Serwer zwrócił odpowiedź, której nie da się sparsować jako JSON", e);
        } catch (RestClientException e) {
            logger.error("Błąd podczas POST request do {}: {}", url, e.getMessage());
            throw new RuntimeException("Nie udało się wysłać żądania POST do: " + url, e);
        }
    }
}
