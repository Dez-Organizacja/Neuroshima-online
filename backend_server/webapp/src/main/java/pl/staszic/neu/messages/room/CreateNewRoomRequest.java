package pl.staszic.neu.messages.room;

public class CreateNewRoomRequest extends RoomScopedWebSocketMessage {

    public static final String TYPE = "CREATENEWROOM_REQUEST";

    public CreateNewRoomRequest() {
        super(TYPE);
    }
}

