package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class LeaveRoomResponse extends WebSocketMessage {

    public static final String TYPE = "LEAVEROOM_RESPONSE";

    @JsonProperty("serverStatus")
    private String serverStatus;

    public LeaveRoomResponse() {
        super(TYPE);
    }

    public String getServerStatus() {
        return serverStatus;
    }

    public void setServerStatus(String serverStatus) {
        this.serverStatus = serverStatus;
    }
}

