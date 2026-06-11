package pl.staszic.neu.messages.room;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import pl.staszic.neu.game.model.RoomMember;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class SetInRoomAttributesResponse extends RoomScopedWebSocketMessage {

    public static final String TYPE = "SETINROOMATTRIBUTES_RESPONSE";

    @JsonProperty("serverStatus")
    private String serverStatus;

    @JsonProperty("error")
    private String error;

    @JsonProperty("faction")
    private String faction;

    @JsonProperty("status")
    private RoomMember.Status status;

    public SetInRoomAttributesResponse() {
        super(TYPE);
    }

    public String getServerStatus() {
        return serverStatus;
    }

    public void setServerStatus(String serverStatus) {
        this.serverStatus = serverStatus;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
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
