package pl.staszic.neu.messages.game;

public class EndGameRequest extends GameScopedWebSocketMessage {

    public static final String TYPE = "ENDGAME_REQUEST";

    public EndGameRequest() {
        super(TYPE);
    }

}

