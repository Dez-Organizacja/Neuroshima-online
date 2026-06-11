package pl.staszic.neu.messages.room;

public class GetRoomStatusRequest extends RoomScopedWebSocketMessage {

    public static final String TYPE = "GETROOMSTATUS_REQUEST";

    public GetRoomStatusRequest() {
        super(TYPE);
    }
}

