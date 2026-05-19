package pl.staszic.neu.messages;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class ApiMessage {

    @JsonProperty("messageType")
    private String messageType;

    @JsonProperty("timestamp")
    private String timestamp;

    protected ApiMessage() {
        this.timestamp = LocalDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME);
    }

    protected ApiMessage(String messageType) {
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

}
