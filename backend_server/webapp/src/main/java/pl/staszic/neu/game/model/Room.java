package pl.staszic.neu.game.model;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public class Room {
    private String roomId;
    private String player1;
    private String player2;
    private String gameId;
    private final Map<String, String> playerFactions = new ConcurrentHashMap<>();

    public Room(String roomId) {
        this.roomId = roomId;
        this.player1 = null;
        this.player2 = null;
    }

    public Room(String roomId, String player1, String player2) {
        this.roomId = roomId;
        this.player1 = player1;
        this.player2 = player2;
    }

    public String getRoomId() {
        return roomId;
    }

    public void setRoomId(String roomId) {
        this.roomId = roomId;
    }

    public String getPlayer1() {
        return player1;
    }

    public void addPlayer(String player) throws Exception {
        if(this.player1 == null) {
            this.player1 = player;
        }
        else if(this.player2 == null) {
            this.player2 = player;
        }
        else {
            throw new Exception("Room is full");
        }
    }

    public void removePlayer(String player) throws Exception {
        if(Objects.equals(this.player1, player)) {
            this.player1 = null;
        }
        else if(Objects.equals(this.player2, player)) {
            this.player2 = null;
        }
        else{
            throw new Exception("There is no such player in the room");
        }
        playerFactions.remove(player);
    }

    public boolean isEmpty() {
        return player1 == null && player2 == null;
    }

    public Set<String> getPlayerIds() {
        Set<String> playerIds = new HashSet<>();
        if(player1 != null) {
            playerIds.add(player1);
        }
        if(player2 != null) {
            playerIds.add(player2);
        }
        return playerIds;
    }

    public String getPlayer2() {
        return player2;
    }

    public String getGameId() {
        return gameId;
    }

    public void setGameId(String gameId) {
        this.gameId = gameId;
    }

    public boolean hasPlayer(String playerId) {
        return Objects.equals(this.player1, playerId) || Objects.equals(this.player2, playerId);
    }

    public boolean hasActiveGame() {
        return gameId != null && !gameId.isBlank();
    }

    public void clearGame() {
        this.gameId = null;
    }

    public boolean isFactionSelectedByAnotherPlayer(String clientId, String faction) {
        for (Map.Entry<String, String> entry : playerFactions.entrySet()) {
            if (!Objects.equals(entry.getKey(), clientId) && Objects.equals(entry.getValue(), faction)) {
                return true;
            }
        }
        return false;
    }

    public void setPlayerFaction(String clientId, String faction) {
        playerFactions.put(clientId, faction);
    }

    public String getPlayerFaction(String clientId) {
        return playerFactions.get(clientId);
    }

    public Map<String, String> getPlayerFactions() {
        return new HashMap<>(playerFactions);
    }
}
