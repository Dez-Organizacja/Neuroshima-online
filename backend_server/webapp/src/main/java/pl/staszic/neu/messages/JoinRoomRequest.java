package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class JoinRoomRequest extends RoomScopedWebSocketMessage {

    public static final String TYPE = "JOINROOM_REQUEST";

    @JsonProperty("playerName")
    private String playerName;

    public JoinRoomRequest() {
        super(TYPE);
    }

    public String getPlayerName() {
        return playerName;
    }

    public void setPlayerName(String playerName) {
        this.playerName = playerName;
    }
}

