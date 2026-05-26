package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.JsonNode;

public class GameViewResponse extends ApiMessage{

    public static final String TYPE = "GAMEVIEW_RESPONSE";

    @JsonProperty("gameView")
    private JsonNode gameView;

    public GameViewResponse() {
        super(TYPE);
    }

    public GameViewResponse(JsonNode gameView) {
        super(TYPE);
        this.gameView = gameView;
    }

    public JsonNode getGameView() {
        return gameView;
    }
    public void setGameView(JsonNode gameView) {
        this.gameView = gameView;
    }

}
