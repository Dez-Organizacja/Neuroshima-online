package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class CreateNewRoomResponse extends WebSocketMessage {
    public static final String TYPE = "CREATENEWROOM_RESPONSE";

    @JsonProperty("createdRoomId")
    private String createdRoomId;

    @JsonProperty("serverStatus")
    private String serverStatus;

    public CreateNewRoomResponse() {
        super(TYPE);
    }

    public String getCreatedRoomId() {
        return createdRoomId;
    }

    public void setCreatedRoomId(String createdRoomId) {
        this.createdRoomId = createdRoomId;
    }

    public String getServerStatus() {
        return serverStatus;
    }

    public void setServerStatus(String serverStatus) {
        this.serverStatus = serverStatus;
    }
}
