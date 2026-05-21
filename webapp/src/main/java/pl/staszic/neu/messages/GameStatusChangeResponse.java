package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.JsonNode;

public class GameStatusChangeResponse extends ApiMessage{

    public static final String TYPE = "GAMESTATUSCHANGE_RESPONSE";

    @JsonProperty("gameState")
    private JsonNode gameState;

    public GameStatusChangeResponse() {
        super(TYPE);
    }

    public GameStatusChangeResponse(JsonNode gameState) {
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
