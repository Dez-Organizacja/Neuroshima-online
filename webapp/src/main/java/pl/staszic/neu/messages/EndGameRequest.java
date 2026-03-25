package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class EndGameRequest extends GameScopedWebSocketMessage {

    public static final String TYPE = "ENDGAME_REQUEST";

    @JsonProperty("winnerId")
    private String winnerId;

    @JsonProperty("reason")
    private String reason;

    public EndGameRequest() {
        super(TYPE);
    }

    public String getWinnerId() {
        return winnerId;
    }

    public void setWinnerId(String winnerId) {
        this.winnerId = winnerId;
    }

    public String getReason() {
        return reason;
    }

    public void setReason(String reason) {
        this.reason = reason;
    }
}

