package pl.staszic.neu.game.model;

import com.fasterxml.jackson.annotation.JsonValue;

public class RoomProperties {

    public enum Visibility {
        PUBLIC("public"),
        PRIVATE("private");

        private final String value;

        Visibility(String value) {
            this.value = value;
        }

        @JsonValue
        public String getValue() {
            return value;
        }
    }

    private Visibility visibility = Visibility.PUBLIC;

    private String host = null;

    public RoomProperties() {}

    public RoomProperties(Visibility visibility) {
        this.visibility = visibility;
    }

    public Visibility getVisibility() {
        return visibility;
    }

    public void setVisibility(Visibility visibility) {
        this.visibility = visibility;
    }

    // Getter i setter dla hosta
    public String getHost() {
        return host;
    }

    public void setHost(String host) {
        this.host = host;
    }
}
