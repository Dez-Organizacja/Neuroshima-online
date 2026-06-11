package pl.staszic.neu.messages.game;

import com.fasterxml.jackson.databind.JsonNode;

public class ActionRequest extends GameScopedWebSocketMessage {

    public static final String TYPE = "ACTION_REQUEST";

    private JsonNode actionData;

    public ActionRequest() {
        super(TYPE);
    }

    public JsonNode getActionData() {
        return actionData;
    }

    public void setActionData(JsonNode actionData) {
        this.actionData = actionData;
    }
}
