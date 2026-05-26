package pl.staszic.neu.messages;

import com.fasterxml.jackson.databind.JsonNode;

public class ActionResponse extends GameScopedWebSocketMessage {

    public static final String TYPE = "ACTION_RESPONSE";

    private JsonNode gameView;

    public ActionResponse() {
        super(TYPE);
    }

    public JsonNode getGameView() {
        return gameView;
    }

    public void setGameView(JsonNode newGameState) {
        this.gameView = newGameState;
    }
}

