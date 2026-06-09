package pl.staszic.neu.game.clientData.service;

import pl.staszic.neu.game.clientData.service.model.ClientData;

public interface ClientDataService {

    void addClientData(String sessionId, ClientData clientData);

    ClientData getClientData(String sessionId);

    void removeClientData(String sessionId);

    String getUsernameBySessionId(String sessionId);

    String getUsernameBySessionIdOrDefault(String sessionId, String defaultUsername);

    String findSessionIdByUsername(String username) throws ClientDataException;

}
