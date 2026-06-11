package pl.staszic.neu.messages.room;

import com.fasterxml.jackson.annotation.JsonProperty;
import pl.staszic.neu.game.model.RoomMember;

public class SetInRoomAttributesRequest extends RoomScopedWebSocketMessage {

    public static final String TYPE = "SETINROOMATTRIBUTES_REQUEST";

    @JsonProperty("faction")
    private String faction;

    @JsonProperty("status")
    private RoomMember.Status status;

    public SetInRoomAttributesRequest() {
        super(TYPE);
    }

    public String getFaction() {
        return faction;
    }

    public void setFaction(String faction) {
        this.faction = faction;
    }

    public RoomMember.Status getStatus() {
        return status;
    }

    public void setStatus(RoomMember.Status status) {
        this.status = status;
    }
}
