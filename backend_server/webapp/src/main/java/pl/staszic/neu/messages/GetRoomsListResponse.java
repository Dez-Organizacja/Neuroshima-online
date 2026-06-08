package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;
import pl.staszic.neu.game.model.RoomBrowserView;

import java.util.Set;

public class GetRoomsListResponse extends WebSocketMessage{

    public static final String TYPE = "GETROOMSLIST_RESPONSE";

    @JsonProperty("serverStatus")
    private String serverStatus;

    @JsonProperty("roomsList")
    private Set<RoomBrowserView> roomsList;

    public GetRoomsListResponse(){ super(TYPE);}

    public void setRoomsList(Set<RoomBrowserView> roomsList){
        this.roomsList = roomsList;
    }
    public Set<RoomBrowserView> getRoomsList(){
        return roomsList;
    }
    public String getServerStatus() {
        return serverStatus;
    }

    public void setServerStatus(String serverStatus) {
        this.serverStatus = serverStatus;
    }
}
