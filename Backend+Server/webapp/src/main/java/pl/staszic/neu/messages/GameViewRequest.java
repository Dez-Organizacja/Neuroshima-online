package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.JsonNode;

public class GameViewRequest extends ApiMessage{

    public static final String TYPE = "GAMEVIEW_REQUEST";

    @JsonProperty("gameState")
    private JsonNode gameState;

    public GameViewRequest() {
        super(TYPE);
    }

    public GameViewRequest(JsonNode gameState, JsonNode userAction) {
        super(TYPE);
        this.gameState = gameState;
    }

    public JsonNode getGameState() {
        return gameState;
    }
    public void setGameState(JsonNode gameState) {
        this.gameState = gameState;
    }

}
