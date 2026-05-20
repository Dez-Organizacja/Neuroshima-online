package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class CreateNewRoomRequest extends WebSocketMessage {

    public static final String TYPE = "CREATENEWROOM_REQUEST";

    @JsonProperty("roomId")
    private String roomId;

    @JsonProperty("playerName")
    private String playerName;


    public CreateNewRoomRequest() {
        super(TYPE);
    }

    public String getPlayerName() {
        return playerName;
    }

    public void setPlayerName(String playerName) {
        this.playerName = playerName;
    }

    public String getRoomId() {
        return roomId;
    }

    public void setRoomId(String roomId) {
        this.roomId = roomId;
    }
}

