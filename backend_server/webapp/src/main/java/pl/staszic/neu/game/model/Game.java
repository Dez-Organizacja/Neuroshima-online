package pl.staszic.neu.game.model;

import com.fasterxml.jackson.databind.JsonNode;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

public class Game {
    private String gameId;

    JsonNode gameState;

    private String currentFaction;

    Map<String, String> playerFactions = new ConcurrentHashMap<>();

    public Game(){
        this.gameId = UUID.randomUUID().toString();
        this.gameState = null;
        this.currentFaction = null;
    }

    public Game(String gameId, JsonNode gameState){
        this.gameId = gameId;
        setGameState(gameState);
    }

    public String getGameId(){
        return gameId;
    }

    public void setGameId(String gameId){
        this.gameId = gameId;
    }

    public JsonNode getGameState() {
        return gameState;
    }

    public void setGameState(JsonNode gameState) {
        this.gameState = gameState;
        JsonNode currentFactionNode = gameState.get("currentFaction");
        this.currentFaction = null;
        if(currentFactionNode != null && currentFactionNode.isTextual()) {
            this.currentFaction = currentFactionNode.asText();
        }
    }

    public String getCurrentFaction() {
        return currentFaction;
    }

    public void setCurrentFaction(String currentFaction) {
        this.currentFaction = currentFaction;
    }

    public Map<String, String> getPlayerFactions() {
        return playerFactions;
    }

    public String getPlayerFaction(String playerId) {
        return playerFactions.get(playerId);
    }

    public void setPlayerFactions(Map<String, String> playerFactions) {
        this.playerFactions = playerFactions;
    }
}
