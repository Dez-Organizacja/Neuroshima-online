package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public abstract class RoomScopedWebSocketMessage extends WebSocketMessage {

    @JsonProperty("roomId")
    private String roomId;

    protected RoomScopedWebSocketMessage() {
        super();
    }

    protected RoomScopedWebSocketMessage(String messageType) {
        super(messageType);
    }

    public String getRoomId() {
        return roomId;
    }

    public void setRoomId(String roomId) {
        this.roomId = roomId;
    }
}

