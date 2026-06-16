package pl.staszic.neu.messages.game;

import pl.staszic.neu.messages.room.RoomScopedWebSocketMessage;

public class GameRemovedNotification extends RoomScopedWebSocketMessage {

    public static final String TYPE = "GAME_REMOVED";

    private String gameId;

    public GameRemovedNotification() {
        super(TYPE);
    }

    public String getGameId() {
        return gameId;
    }

    public void setGameId(String gameId) {
        this.gameId = gameId;
    }
}
