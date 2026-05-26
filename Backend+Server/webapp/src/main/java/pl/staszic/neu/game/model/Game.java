package pl.staszic.neu.game.model;

import com.fasterxml.jackson.databind.JsonNode;

import java.util.UUID;

public class Game {
    private String gameId;

    JsonNode gameState;

    public Game(){
        this.gameId = UUID.randomUUID().toString();
        this.gameState = null;
    }

    public Game(String gameId, JsonNode gameState){
        this.gameId = gameId;
        this.gameState = gameState;
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
    }
}
