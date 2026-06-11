package pl.staszic.neu.messages.api;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.JsonNode;

public class GameStatusChangeRequest extends ApiMessage {

    public static final String TYPE = "GAMESTATUSCHANGE_REQUEST";

    @JsonProperty("gameState")
    private JsonNode gameState;

    @JsonProperty("userAction")
    private JsonNode userAction;

    public GameStatusChangeRequest() {
        super(TYPE);
    }

    public GameStatusChangeRequest(JsonNode gameState, JsonNode userAction) {
        super(TYPE);
        this.gameState = gameState;
        this.userAction = userAction;
    }

    public JsonNode getGameState() {
        return gameState;
    }
    public void setGameState(JsonNode gameState) {
        this.gameState = gameState;
    }

    public JsonNode getUserAction() {
        return userAction;
    }
    public void setUserAction(JsonNode userAction) {
        this.userAction = userAction;
    }

}
