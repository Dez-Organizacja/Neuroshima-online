package pl.staszic.neu.messages.room;

import com.fasterxml.jackson.annotation.JsonProperty;

public class LeaveRoomRequest extends RoomScopedWebSocketMessage {

    public static final String TYPE = "LEAVEROOM_REQUEST";

    @JsonProperty("playerName")
    private String playerName;

    public LeaveRoomRequest() {
        super(TYPE);
    }

    public String getPlayerName() {
        return playerName;
    }

    public void setPlayerName(String playerName) {
        this.playerName = playerName;
    }
}

