package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class EndGameResponse extends GameScopedWebSocketMessage {

    public static final String TYPE = "ENDGAME_RESPONSE";

    @JsonProperty("ended")
    private boolean ended;

    @JsonProperty("summary")
    private String summary;

    public EndGameResponse() {
        super(TYPE);
    }

    public boolean isEnded() {
        return ended;
    }

    public void setEnded(boolean ended) {
        this.ended = ended;
    }

    public String getSummary() {
        return summary;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }
}

