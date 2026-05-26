package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Bazowa klasa komunikatu websocket.
 * Każdy komunikat dziedziczący posiada typ, czas utworzenia i identyfikator klienta.
 */
public abstract class WebSocketMessage {

    @JsonProperty("messageType")
    private String messageType;

    @JsonProperty("timestamp")
    private String timestamp;

    @JsonProperty("clientId")
    private String clientId;

    protected WebSocketMessage() {
        this.timestamp = LocalDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME);
    }

    protected WebSocketMessage(String messageType) {
        this();
        this.messageType = messageType;
    }

    public String getMessageType() {
        return messageType;
    }

    public void setMessageType(String messageType) {
        this.messageType = messageType;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public String getClientId() {
        return clientId;
    }

    public void setClientId(String clientId) {
        this.clientId = clientId;
    }
}

