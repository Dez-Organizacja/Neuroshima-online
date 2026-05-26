package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.JsonNode;

public class NewGameRequest extends WebSocketMessage {

    public static final String TYPE = "NEWGAME_REQUEST";

    @JsonProperty("roomId")
    private String roomId;

    @JsonProperty("scenario")
    private JsonNode scenario;

    public NewGameRequest() {
        super(TYPE);
    }

    public JsonNode getScenario() {
        return scenario;
    }

    public void setScenario(JsonNode scenario) {
        this.scenario = scenario;
    }

    public String getRoomId() {
        return roomId;
    }

    public void setRoomId(String roomId) {
        this.roomId = roomId;
    }
}

