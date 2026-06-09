package pl.staszic.neu.game.clientData.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import pl.staszic.neu.game.clientData.service.model.ClientData;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class InMemoryClientDataService implements ClientDataService {
    private static final Logger logger = LoggerFactory.getLogger(InMemoryClientDataService.class);

    private final Map<String, ClientData> clientDataMap = new ConcurrentHashMap<>();

    @Autowired
    public InMemoryClientDataService() {}

    @Override
    public void addClientData(String sessionId, ClientData clientData) {
        clientDataMap.put(sessionId, clientData);
    }

    @Override
    public ClientData getClientData(String sessionId) {
        if(!clientDataMap.containsKey(sessionId)) {
            throw new ExceptionInInitializerError("No client data found for sessionId: " + sessionId);
        }
        return clientDataMap.get(sessionId);
    }

    @Override
    public void removeClientData(String sessionId) {
        if(!clientDataMap.containsKey(sessionId)) {
            logger.warn("No client data found for sessionId: {}", sessionId);
            return;
        }
        clientDataMap.remove(sessionId);
    }

    @Override
    public String getUsernameBySessionId(String sessionId) {
        return clientDataMap.get(sessionId).getUsername();
    }

    @Override
    public String getUsernameBySessionIdOrDefault(String sessionId, String defaultUsername) {
        return clientDataMap.getOrDefault(sessionId, new ClientData(defaultUsername)).getUsername();
    }

    @Override
    public String findSessionIdByUsername(String username) throws ClientDataException {
        String sessionId = clientDataMap.entrySet().stream()
                .filter(entry -> entry.getValue().getUsername().equals(username))
                .map(Map.Entry::getKey)
                .findFirst()
                .orElse(null);
        if (sessionId == null) {
            throw new ClientDataException("No sessionId found for username: " + username);
        }
        return sessionId;
    }
}
