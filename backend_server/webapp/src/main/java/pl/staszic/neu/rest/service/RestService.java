package pl.staszic.neu.rest.service;

import com.fasterxml.jackson.databind.JsonNode;

public interface RestService {

    JsonNode postJson(String url, JsonNode requestBody);

}
