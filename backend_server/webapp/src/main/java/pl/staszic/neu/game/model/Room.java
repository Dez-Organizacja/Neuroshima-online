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

    public void mergePlayerAttributes(String clientId, RoomMember roomMember) {
        if(!players.containsKey(clientId)) {
            throw new IllegalArgumentException("Player not in the room");
        }
        players.get(clientId).setFaction(roomMember.getFaction());
        players.get(clientId).setStatus(roomMember.getStatus());
    }

    public String getPlayerFaction(String clientId) {
        return players.get(clientId).getFaction();
    }

    public Set<String> getFactions(){
        Set<String> factions = new HashSet<>();
        int playerCount = 0;
        for(Map.Entry<String, RoomMember> entry : players.entrySet()) {
            if(entry.getValue().getStatus() != RoomMember.Status.ACTIVE) {
                continue;
            }
            playerCount++;
            factions.add(entry.getValue().getFaction());
        }

        if(playerCount != factions.size()) {
            throw new IllegalStateException("Players need to choose different factions");
        }

        return factions;
    }

    public Map<String, String> getActivePlayerFactions() {
        Map<String, String> factions = new HashMap<>();
        for(Map.Entry<String, RoomMember> entry : players.entrySet()) {
            if(entry.getValue().getStatus() != RoomMember.Status.ACTIVE) {
                continue;
            }
            factions.put(entry.getKey(), entry.getValue().getFaction());
        }

        return factions;
    }

    public Map<String, String> getAllPlayerFactions() {
        Map<String, String> factions = new HashMap<>();
        for(Map.Entry<String, RoomMember> entry : players.entrySet()) {
            factions.put(entry.getKey(), entry.getValue().getFaction());
        }

        return factions;
    }
}
