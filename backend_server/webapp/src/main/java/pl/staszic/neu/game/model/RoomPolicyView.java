package pl.staszic.neu.game.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class RoomPolicyView {

    @JsonProperty("visibility")
    private RoomPolicy.Visibility visibility;

    @JsonProperty("host")
    private String hostUsername;

    public RoomPolicyView() {}

    public RoomPolicyView(RoomPolicy.Visibility visibility, String hostUsername) {
        this.visibility = visibility;
        this.hostUsername = hostUsername;
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
