package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class GetRoomStatusRequest extends WebSocketMessage{

    public static final String TYPE = "GETROOMSTATUS_REQUEST";

    @JsonProperty("roomId")
    private String roomId;

    public GetRoomStatusRequest() {
        super(TYPE);
    }

    public void setRoomId(String roomId) {
        this.roomId = roomId;
    }

    public String getRoomId(){
        return roomId;
    }
}

