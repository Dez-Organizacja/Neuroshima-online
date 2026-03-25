package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class EndTurnRequest extends GameScopedWebSocketMessage {

    public static final String TYPE = "ENDTURN_REQUEST";

    @JsonProperty("playerId")
    private String playerId;

    @JsonProperty("turnNumber")
    private int turnNumber;

    public EndTurnRequest() {
        super(TYPE);
    }

    public String getPlayerId() {
        return playerId;
    }

    public void setPlayerId(String playerId) {
        this.playerId = playerId;
    }

    public int getTurnNumber() {
        return turnNumber;
    }

    public void setTurnNumber(int turnNumber) {
        this.turnNumber = turnNumber;
    }
}

