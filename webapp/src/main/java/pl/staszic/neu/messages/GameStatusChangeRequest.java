package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;
import pl.staszic.neu.game.model.GameData;

public class GameStatusChangeRequest extends ApiMessage {

    @JsonProperty("data")
    GameData data;

    public GameStatusChangeRequest() { }

    public GameStatusChangeRequest(GameData data) {
        this.data = data;
    }

    public GameData getData() {
        return data;
    }
    public void setData(GameData data) {
        this.data = data;
    }

}
