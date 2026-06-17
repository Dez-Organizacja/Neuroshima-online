package pl.staszic.neu.messages.room;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.JsonNode;
import pl.staszic.neu.game.model.RoomPolicyView;

import java.util.Map;
import java.util.Set;

public class GetRoomStatusResponse extends RoomScopedWebSocketMessage {

    public static final String TYPE = "GETROOMSTATUS_RESPONSE";

    @JsonProperty("serverStatus")
    private String serverStatus;

    @JsonProperty("playersInRoom")
    private Set<String> playersInRoom;

    @JsonProperty("playerFactions")
    private Map<String, String> playerFactions;

    @JsonProperty("gameId")
    private String gameId;

    @JsonProperty("roomPolicy")
    private RoomPolicyView roomPolicyView;

    @JsonProperty("gameView")
    private JsonNode gameView;

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

    public Map<String, String> getPlayerFactions() {
        return playerFactions;
    }

    public void setPlayerFactions(Map<String, String> playerFactions) {
        this.playerFactions = playerFactions;
    }

    public void setGameId(String gameId) {
        this.gameId = gameId;
    }
    public String getGameId() {
        return gameId;
    }

    public RoomPolicyView getRoomPolicyView() {
        return roomPolicyView;
    }

    public void setRoomPolicyView(RoomPolicyView roomPolicyView) {
        this.roomPolicyView = roomPolicyView;
    }

    public JsonNode getGameView() {
        return gameView;
    }

    public void setGameView(JsonNode gameView) {
        this.gameView = gameView;
    }
}
