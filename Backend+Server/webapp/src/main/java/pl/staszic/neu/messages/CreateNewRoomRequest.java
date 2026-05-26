package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class CreateNewRoomRequest extends WebSocketMessage {

    public static final String TYPE = "CREATENEWROOM_REQUEST";

    @JsonProperty("roomId")
    private String roomId;

    public CreateNewRoomRequest() {
        super(TYPE);
    }

    public String getRoomId() {
        return roomId;
    }

    public void setRoomId(String roomId) {
        this.roomId = roomId;
    }
}

