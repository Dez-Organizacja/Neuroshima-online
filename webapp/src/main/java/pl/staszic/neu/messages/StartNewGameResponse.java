package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class StartNewGameResponse extends WebSocketMessage {

    public static final String TYPE = "STARTNEWGAME_RESPONSE";

    @JsonProperty("createdGameId")
    private String createdGameId;

    @JsonProperty("serverStatus")
    private String serverStatus;

    public StartNewGameResponse() {
        super(TYPE);
    }

    public String getCreatedGameId() {
        return createdGameId;
    }

    public void setCreatedGameId(String createdGameId) {
        this.createdGameId = createdGameId;
    }

    public String getServerStatus() {
        return serverStatus;
    }

    public void setServerStatus(String serverStatus) {
        this.serverStatus = serverStatus;
    }
}

