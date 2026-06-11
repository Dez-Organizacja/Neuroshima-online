package pl.staszic.neu.messages.game;

public class EndGameResponse extends GameScopedWebSocketMessage {

    public static final String TYPE = "ENDGAME_RESPONSE";

    public EndGameResponse() {
        super(TYPE);
    }

}

