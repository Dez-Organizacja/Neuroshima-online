package pl.staszic.neu.messages.room;

import com.fasterxml.jackson.annotation.JsonProperty;
import pl.staszic.neu.messages.WebSocketMessage;

public class KickFromRoomResponse extends RoomScopedWebSocketMessage {
    public static final String TYPE = "KICKFROMROOM_RESPONSE";

    @JsonProperty("serverStatus")
    private String serverStatus;

    @JsonProperty("kicker")
    private String kickerUsername;

    public KickFromRoomResponse() {
        super(TYPE);
    }

    public KickFromRoomResponse(String kickerUsername) {
        super(TYPE);
        this.kickerUsername = kickerUsername;
    }

    public String getKickerUsername() {
        return kickerUsername;
    }

    public void setKickerUsername(String kickerUsername) {
        this.kickerUsername = kickerUsername;
    }

    public String getServerStatus() {
        return serverStatus;
    }

    public void setServerStatus(String serverStatus) {
        this.serverStatus = serverStatus;
    }
}
