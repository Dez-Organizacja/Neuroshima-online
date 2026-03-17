package org.example;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Klasa reprezentująca wiadomość WebSocket w formacie JSON.
 * Zawiera następujące pola:
 * - type: typ komunikatu (connection, disconnection, message)
 * - timestamp: czas wysłania komunikatu w formacie ISO-8601
 * - clientId: unikalny identyfikator klienta
 * - message: treść wiadomości (opcjonalnie, tylko dla typu "message")
 */
public class WebSocketMessage {
    // Typy komunikatów
    public enum MessageType {
        CONNECTION("connection"),
        DISCONNECTION("disconnection"),
        MESSAGE("message"),
        ECHO("echo");

        private final String value;

        MessageType(String value) {
            this.value = value;
        }

        public String getValue() {
            return value;
        }
    }

    @JsonProperty("type")
    private String type;

    @JsonProperty("timestamp")
    private String timestamp;

    @JsonProperty("clientId")
    private String clientId;

    @JsonProperty("message")
    private String message;

    /**
     * Konstruktor domyślny - wymagany dla deserializacji JSON
     */
    public WebSocketMessage() {
        this.timestamp = LocalDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME);
    }

    /**
     * Konstruktor do tworzenia wiadomości z typem, clientId i opcjonalną treścią
     * @param type typ komunikatu
     * @param clientId unikalny identyfikator klienta
     * @param message treść wiadomości (opcjonalnie)
     */
    public WebSocketMessage(MessageType type, String clientId, String message) {
        this.type = type.getValue();
        this.clientId = clientId;
        this.message = message;
        this.timestamp = LocalDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME);
    }

    // Gettery i settery
    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
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

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    @Override
    public String toString() {
        return "WebSocketMessage{" +
                "type='" + type + '\'' +
                ", timestamp='" + timestamp + '\'' +
                ", clientId='" + clientId + '\'' +
                ", message='" + message + '\'' +
                '}';
    }
}

