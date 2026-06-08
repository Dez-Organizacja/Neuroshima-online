package pl.staszic.neu.game.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class RoomPropertiesView {

    @JsonProperty("visibility")
    private RoomProperties.Visibility visibility;

    @JsonProperty("host")
    private String hostUsername;

    public RoomPropertiesView() {}

    public RoomPropertiesView(RoomProperties.Visibility visibility, String hostUsername) {
        this.visibility = visibility;
        this.hostUsername = hostUsername;
    }

    public RoomProperties.Visibility getVisibility() {
        return visibility;
    }

    public void setVisibility(RoomProperties.Visibility visibility) {
        this.visibility = visibility;
    }

    public String getHostUsername() {
        return hostUsername;
    }

    public void setHostUsername(String hostUsername) {
        this.hostUsername = hostUsername;
    }
}
