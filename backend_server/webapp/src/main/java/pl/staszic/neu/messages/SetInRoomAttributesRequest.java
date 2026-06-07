package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class SetInRoomAttributesRequest extends RoomScopedWebSocketMessage {

    public static final String TYPE = "SETINROOMATTRIBUTES_REQUEST";

    @JsonProperty("faction")
    private String faction;

    @JsonProperty("status")
    private String status;

    public SetInRoomAttributesRequest() {
        super(TYPE);
    }

    public String getFaction() {
        return faction;
    }

    public void setFaction(String faction) {
        this.faction = faction;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
