package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.Set;

public class GetRoomStatusResponse extends WebSocketMessage {

    public static final String TYPE = "GETROOMSTATUS_RESPONSE";

    @JsonProperty("serverStatus")
    private String serverStatus;

    @JsonProperty("roomId")
    private String roomId;

    @JsonProperty("playersInRoom")
    private Set<String> playersInRoom;

    @JsonProperty("gameId")
    private String gameId;

    public GetRoomStatusResponse() {
        super(TYPE);
    }

    public String getServerStatus() {
        return serverStatus;
    }

    public void setServerStatus(String serverStatus) {
        this.serverStatus = serverStatus;
    }

    public Set<String> getPlayersInRoom() {
        return playersInRoom;
    }

    public void setPlayersInRoom(Set<String> playersInRoom) {
        this.playersInRoom = playersInRoom;
    }

    public String getRoomId() {
        return roomId;
    }
    public void setRoomId(String roomId) {
        this.roomId = roomId;
    }

    public void setGameId(String gameId) {
        this.gameId = gameId;
    }
    public String getGameId() {
        return gameId;
    }
}

