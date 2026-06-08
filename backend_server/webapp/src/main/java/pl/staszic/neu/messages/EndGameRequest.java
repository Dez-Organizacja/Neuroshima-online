package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class EndGameRequest extends GameScopedWebSocketMessage {

    public static final String TYPE = "ENDGAME_REQUEST";

    public EndGameRequest() {
        super(TYPE);
    }

}

