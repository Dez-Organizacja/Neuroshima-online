package pl.staszic.neu.messages;

public class GetUserDataRequest extends WebSocketMessage {

    public static final String TYPE = "GETUSERDATA_REQUEST";

    public GetUserDataRequest() { super(TYPE); }
}
