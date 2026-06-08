package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class EndGameResponse extends GameScopedWebSocketMessage {

    public static final String TYPE = "ENDGAME_RESPONSE";

    public EndGameResponse() {
        super(TYPE);
    }

}

