package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class StartNewGameRequest extends WebSocketMessage {

    public static final String TYPE = "STARTNEWGAME_REQUEST";

    @JsonProperty("playerName")
    private String playerName;

    @JsonProperty("scenario")
    private String scenario;


    public StartNewGameRequest() {
        super(TYPE);
    }

    public String getPlayerName() {
        return playerName;
    }

    public void setPlayerName(String playerName) {
        this.playerName = playerName;
    }

    public String getScenario() {
        return scenario;
    }

    public void setScenario(String scenario) {
        this.scenario = scenario;
    }
}

