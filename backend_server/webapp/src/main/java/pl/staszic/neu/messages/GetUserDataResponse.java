package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

public class GetUserDataResponse extends WebSocketMessage{

    public static final String TYPE = "GETUSERDATA_RESPONSE";

    @JsonProperty("serverStatus")
    private String serverStatus;

    @JsonProperty("error")
    private String error;

    @JsonProperty("username")
    private String username;

    @JsonProperty("matches")
    private Integer matches;

    @JsonProperty("wins")
    private Integer wins;

    public GetUserDataResponse() { super(TYPE); }

    public String getUsername() {
        return username;
    }
    public void setUsername(String username) {
        this.username = username;
    }

    public Integer getMatches() {
        return matches;
    }
    public void setMatches(Integer matches) {
        this.matches = matches;
    }
    public Integer getWins() {
        return wins;
    }
    public void setWins(Integer wins) {
        this.wins = wins;
    }

    public String getError(){
        return this.error;
    }
    public void setError(String error){
        this.error = error;
    }
    public String getServerStatus() {
        return serverStatus;
    }
    public void setServerStatus(String serverStatus) {
        this.serverStatus = serverStatus;
    }
}
