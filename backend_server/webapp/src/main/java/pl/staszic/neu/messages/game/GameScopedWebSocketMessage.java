package pl.staszic.neu.messages.game;

import com.fasterxml.jackson.annotation.JsonProperty;
import pl.staszic.neu.messages.WebSocketMessage;

/**
 * Bazowa klasa dla komunikatow odnoszacych sie do konkretnej gry.
 */
public abstract class GameScopedWebSocketMessage extends WebSocketMessage {

    @JsonProperty("gameId")
    private String gameId;

    protected GameScopedWebSocketMessage() {
        super();
    }

    protected GameScopedWebSocketMessage(String messageType) {
        super(messageType);
    }

    public String getGameId() {
        return gameId;
    }

    public void setGameId(String gameId) {
        this.gameId = gameId;
    }
}

