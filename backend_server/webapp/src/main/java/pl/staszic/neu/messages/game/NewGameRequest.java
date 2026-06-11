package pl.staszic.neu.messages.game;

import com.fasterxml.jackson.annotation.JsonProperty;
import pl.staszic.neu.messages.WebSocketMessage;

public class NewGameRequest extends WebSocketMessage {

    public static final String TYPE = "NEWGAME_REQUEST";

    @JsonProperty("roomId")
    private String roomId;

    public NewGameRequest() {
        super(TYPE);
    }

    public String getRoomId() {
        return roomId;
    }

    public void setRoomId(String roomId) {
        this.roomId = roomId;
    }
}

