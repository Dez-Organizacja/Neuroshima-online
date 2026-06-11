package pl.staszic.neu.messages.game;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.JsonNode;
import pl.staszic.neu.messages.WebSocketMessage;

public class NewGameResponse extends WebSocketMessage {

    public static final String TYPE = "NEWGAME_RESPONSE";

    @JsonProperty("createdGameId")
    private String createdGameId;

    @JsonProperty("roomId")
    private String roomId;

    @JsonProperty("serverStatus")
    private String serverStatus;

    @JsonProperty("gameView")
    private JsonNode gameView;

    public NewGameResponse() {
        super(TYPE);
    }

    public String getCreatedGameId() {
        return createdGameId;
    }

    public void setCreatedGameId(String createdGameId) {
        this.createdGameId = createdGameId;
    }

    public String getServerStatus() {
        return serverStatus;
    }

    public void setServerStatus(String serverStatus) {
        this.serverStatus = serverStatus;
    }

    public String getRoomId() {
        return roomId;
    }

    public void setRoomId(String roomId) {
        this.roomId = roomId;
    }

    public JsonNode getGameView() {
        return gameView;
    }

    public void setGameView(JsonNode gameView) {
        this.gameView = gameView;
    }
}

