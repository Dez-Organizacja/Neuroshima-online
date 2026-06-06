package pl.staszic.neu.game.model;

public class RoomMember {

    public enum Status {
        ACTIVE,
        SPECTATING
    }

    private String roomId = null;
    private String clientId = null;
    private String faction = null;
    private Status status = Status.SPECTATING;

    RoomMember() {
    }

    RoomMember(String roomId, String clientId, String faction) {
        this.roomId = roomId;
        this.clientId = clientId;
        this.faction = faction;
        this.status = Status.ACTIVE;
    }

    public String getRoomId() {
        return roomId;
    }

    public void setRoomId(String roomId) {
        this.roomId = roomId;
    }

    public String getClientId() {
        return clientId;
    }

    public void setClientId(String clientId) {
        this.clientId = clientId;
    }

    public String getFaction() {
        return faction;
    }

    public void setFaction(String faction) {
        this.faction = faction;
    }

    public Status getStatus() {
        return status;
    }

    public void setStatus(Status status) {
        this.status = status;
    }

}
