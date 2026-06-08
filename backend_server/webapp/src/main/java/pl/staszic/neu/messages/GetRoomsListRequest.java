package pl.staszic.neu.messages;

public class GetRoomsListRequest extends WebSocketMessage{

    public static final String TYPE = "GETROOMSLIST_REQUEST";

    public GetRoomsListRequest() {
        super(TYPE);
    }
}
