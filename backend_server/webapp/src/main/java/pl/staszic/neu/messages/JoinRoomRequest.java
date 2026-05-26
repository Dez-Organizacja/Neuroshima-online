package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class JoinRoomRequest extends WebSocketMessage {

    public static final String TYPE = "JOINROOM_REQUEST";

    @JsonProperty("playerName")
    private String playerName;

    @JsonProperty("roomId")
    private String roomId;

    public JoinRoomRequest() {
        super(TYPE);
    }

    public String getPlayerName() {
        return playerName;
    }

    public void setPlayerName(String playerName) {
        this.playerName = playerName;
    }

    public void setRoomId(String roomId) {
        this.roomId = roomId;
    }

    public String getRoomId(){
        return roomId;
    }
}

