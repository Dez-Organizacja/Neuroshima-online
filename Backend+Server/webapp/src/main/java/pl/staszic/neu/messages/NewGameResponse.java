package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class NewGameResponse extends WebSocketMessage {

    public static final String TYPE = "NEWGAME_RESPONSE";

    @JsonProperty("createdGameId")
    private String createdGameId;

    @JsonProperty("roomId")
    private String roomId;

    @JsonProperty("serverStatus")
    private String serverStatus;

    public NewGameResponse() {
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

    public String getRoomId() {
        return roomId;
    }

    public void setRoomId(String roomId) {
        this.roomId = roomId;
    }
}

