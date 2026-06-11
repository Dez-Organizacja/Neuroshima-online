package pl.staszic.neu.messages.room;

import com.fasterxml.jackson.annotation.JsonProperty;

public class KickFromRoomRequest extends RoomScopedWebSocketMessage {

    public static final String TYPE = "KICKFROMROOM_REQUEST";

    @JsonProperty("kickedPlayer")
    private String kickedPlayerUsername;

    public KickFromRoomRequest() {
        super(TYPE);
    }

    public String getKickedPlayerUsername() {
        return kickedPlayerUsername;
    }

    public void setKickedPlayerUsername(String kickedPlayerUsername) {
        this.kickedPlayerUsername = kickedPlayerUsername;
    }

}
