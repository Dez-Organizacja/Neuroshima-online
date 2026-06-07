package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class SetInRoomAttributesResponse extends WebSocketMessage {

    public static final String TYPE = "SETINROOMATTRIBUTES_RESPONSE";

    @JsonProperty("serverStatus")
    private String serverStatus;

    @JsonProperty("error")
    private String error;

    @JsonProperty("faction")
    private String faction;

    @JsonProperty("status")
    private String status;

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

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
