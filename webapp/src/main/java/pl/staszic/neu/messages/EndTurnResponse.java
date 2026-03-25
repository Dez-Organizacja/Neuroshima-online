package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class EndTurnResponse extends GameScopedWebSocketMessage {

    public static final String TYPE = "ENDTURN_RESPONSE";

    @JsonProperty("accepted")
    private boolean accepted;

    @JsonProperty("nextPlayerId")
    private String nextPlayerId;

    public EndTurnResponse() {
        super(TYPE);
    }

    public boolean isAccepted() {
        return accepted;
    }

    public void setAccepted(boolean accepted) {
        this.accepted = accepted;
    }

    public String getNextPlayerId() {
        return nextPlayerId;
    }

    public void setNextPlayerId(String nextPlayerId) {
        this.nextPlayerId = nextPlayerId;
    }
}

