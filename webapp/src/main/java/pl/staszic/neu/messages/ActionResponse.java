package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.JsonNode;

public class ActionResponse extends GameScopedWebSocketMessage {

    public static final String TYPE = "ACTION_RESPONSE";

    private JsonNode gameState;

    public ActionResponse() {
        super(TYPE);
    }

    public JsonNode getGameState() {
        return gameState;
    }

    public void setGameState(JsonNode newGameState) {
        this.gameState = newGameState;
    }
}

