package pl.staszic.neu.messages;

import com.fasterxml.jackson.databind.JsonNode;

public class ActionRequest extends GameScopedWebSocketMessage {

    public static final String TYPE = "ACTION_REQUEST";

    private String playerId;
    private JsonNode actionData;

    public ActionRequest() {
        super(TYPE);
    }

    public String getPlayerId() {
        return playerId;
    }

    public void setPlayerId(String playerId) {
        this.playerId = playerId;
    }

    public JsonNode getActionData() {
        return actionData;
    }

    public void setActionData(JsonNode actionData) {
        this.actionData = actionData;
    }
}
