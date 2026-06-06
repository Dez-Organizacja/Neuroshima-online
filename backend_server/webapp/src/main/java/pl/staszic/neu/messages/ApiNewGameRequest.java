package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.JsonNode;

public class ApiNewGameRequest extends ApiMessage {

    public static final String TYPE = "NEWGAME_REQUEST";

    @JsonProperty("factions")
    private JsonNode scenario;

    public ApiNewGameRequest() {
        super(TYPE);
    }

    public ApiNewGameRequest(JsonNode scenario) {
        super(TYPE);
        this.scenario = scenario;
    }

    public JsonNode getScenario() {
        return scenario;
    }

    public void setScenario(JsonNode scenario) {
        this.scenario = scenario;
    }

}
