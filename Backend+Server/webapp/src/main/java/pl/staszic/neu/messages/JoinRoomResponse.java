package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class JoinRoomResponse extends WebSocketMessage {

    public static final String TYPE = "JOINROOM_RESPONSE";

    @JsonProperty("serverStatus")
    private String serverStatus;

    public JoinRoomResponse() {
        super(TYPE);
    }

    public String getServerStatus() {
        return serverStatus;
    }

    public void setServerStatus(String serverStatus) {
        this.serverStatus = serverStatus;
    }
}

