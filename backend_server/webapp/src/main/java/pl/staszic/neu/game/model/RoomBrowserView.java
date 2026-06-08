package pl.staszic.neu.game.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class RoomBrowserView {

    @JsonProperty("roomId")
    private String roomId;

    @JsonProperty("membersCount")
    private Integer membersCount;

    @JsonProperty("host")
    private String hostUsername;

    @JsonProperty("visibility")
    RoomPolicy.Visibility visibility;

    public RoomBrowserView() {}

    public RoomBrowserView(String roomId, Integer membersCount, String host, RoomPolicy.Visibility visibility){
        this.roomId = roomId;
        this.membersCount = membersCount;
        this.hostUsername = host;
        this.visibility = visibility;
    }

    public String getRoomId() {
        return roomId;
    }

    public void setRoomId(String roomId) {
        this.roomId = roomId;
    }

    public Integer getMembersCount(){
        return membersCount;
    }

    public void setMembersCount(Integer membersCount){
        this.membersCount = membersCount;
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
