package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;
import pl.staszic.neu.game.model.RoomPolicy;

public class SetRoomPolicyRequest extends RoomScopedWebSocketMessage{

    public static final String TYPE = "SETROOMPOLICY_REQUEST";

    @JsonProperty("visibility")
    RoomPolicy.Visibility visibility;

    @JsonProperty("host")
    String hostUsername;

    public SetRoomPolicyRequest() {
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
}
