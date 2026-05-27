package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class SetFactionRequest extends WebSocketMessage {

    public static final String TYPE = "SETFACTION_REQUEST";

    @JsonProperty("faction")
    private String faction;

    public SetFactionRequest() {
        super(TYPE);
    }

    public String getFaction() {
        return faction;
    }

    public void setFaction(String faction) {
        this.faction = faction;
    }
}
