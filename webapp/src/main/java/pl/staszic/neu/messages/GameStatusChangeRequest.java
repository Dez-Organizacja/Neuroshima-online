package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.JsonNode;

public class GameStatusChangeRequest extends ApiMessage {
    @JsonProperty("gameId")
    private String gameId;

    @JsonProperty("gameState")
    JsonNode gameState;

    @JsonProperty("klik")
    JsonNode klik;

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

    public JsonNode getKlik() {
        return klik;
    }

    public void setKlik(JsonNode klik) {
        this.klik = klik;
    }

}
