package pl.staszic.neu.game.model;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public class Room {
    private String roomId;
    private String gameId;
    private final Map<String, RoomMember> players = new ConcurrentHashMap<>();

    public Room(String roomId) {
        this.roomId = roomId;
    }

    public String getRoomId() {
        return roomId;
    }

    public void setRoomId(String roomId) {
        this.roomId = roomId;
    }

    public void addPlayer(String player) throws Exception {
        if(players.containsKey(player)) {
            throw new Exception("Player already in the room");
        }
        players.put(player, new RoomMember(roomId, player, null));
    }

    public void removePlayer(String player) throws Exception {
        if(!players.containsKey(player)) {
            throw new Exception("Player not in the room");
        }
        players.remove(player);
    }

    public boolean isEmpty() {
        return players.isEmpty();
    }

    public Set<String> getPlayerIds() {
        Set<String> playerIds = new HashSet<>();
        for(Map.Entry<String, RoomMember> entry : players.entrySet()) {
            playerIds.add(entry.getKey());
        }
        return playerIds;
    }

    public String getGameId() {
        return gameId;
    }

    public void setGameId(String gameId) {
        this.gameId = gameId;
    }

    public boolean hasPlayer(String playerId) {
        return players.containsKey(playerId);
    }

    public boolean hasActiveGame() {
        return gameId != null && !gameId.isBlank();
    }

    public void clearGame() {
        this.gameId = null;
    }

    public void setPlayerFaction(String clientId, String faction) {
        if(!players.containsKey(clientId)) {
            throw new IllegalArgumentException("Player not in the room");
        }
        players.get(clientId).setFaction(faction);
    }

    public String getPlayerFaction(String clientId) {
        return players.get(clientId).getFaction();
    }

    public Map<String, String> getScenario(){
        Map<String, String> factions = new HashMap<>();
        Set<String> uniqueFactions = new HashSet<>();
        int playerCount = 0;
        for(Map.Entry<String, RoomMember> entry : players.entrySet()) {
            if(entry.getValue().getStatus() != RoomMember.Status.ACTIVE) {
                continue;
            }
            playerCount++;
            factions.put(entry.getKey(), entry.getValue().getFaction());
            uniqueFactions.add(entry.getValue().getFaction());
        }

        if(playerCount != uniqueFactions.size()) {
            throw new IllegalStateException("Players need to choose different factions");
        }

        return factions;
    }

    public Map<String, String> getPlayerFactions() {
        Map<String, String> factions = new HashMap<>();
        for(Map.Entry<String, RoomMember> entry : players.entrySet()) {
            factions.put(entry.getKey(), entry.getValue().getFaction());
        }

        return factions;
    }
}
