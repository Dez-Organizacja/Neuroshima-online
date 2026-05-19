package pl.staszic.neu.game.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.JsonNode;

public class GameData {

    @JsonProperty("gameState")
    private String gameState;

    @JsonProperty("klik")
    private JsonNode klik;

    public GameData() {}

    public GameData(String gameState, JsonNode klik) {
        this.gameState = gameState;
    }

    public String getGameState() {
        return gameState;
    }
    public void setGameState(String gameState) {
        this.gameState = gameState;
    }

    public JsonNode getKlik() {
        return klik;
    }
    public void setKlik(JsonNode klik) {
        this.klik = klik;
    }

}
