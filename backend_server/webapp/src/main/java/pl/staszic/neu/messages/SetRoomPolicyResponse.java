package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;
import pl.staszic.neu.game.model.RoomPolicy;

public class SetRoomPolicyResponse extends RoomScopedWebSocketMessage{

    public static final String TYPE = "SETROOMPOLICY_RESPONSE";

    @JsonProperty("serverStatus")
    private String serverStatus;

    @JsonProperty("error")
    private String error;

    @JsonProperty("visibility")
    RoomPolicy.Visibility visibility;

    @JsonProperty("host")
    String hostUsername;

    public SetRoomPolicyResponse() {
        super(TYPE);
    }

    public RoomPolicy.Visibility getVisibility() {
        return visibility;
    }
    public void setVisibility(RoomPolicy.Visibility visibility) {
        this.visibility = visibility;
    }
    public String getHostUsername() {
        return hostUsername;
    }
    public void setHostUsername(String hostUsername) {
        this.hostUsername = hostUsername;
    }
    public String getError(){
        return this.error;
    }
    public void setError(String error){
        this.error = error;
    }
    public String getServerStatus() {
        return serverStatus;
    }

    public void setServerStatus(String serverStatus) {
        this.serverStatus = serverStatus;
    }
}
