package pl.staszic.neu.game.service;

public class GameValidationException extends RuntimeException {
    public GameValidationException(String message) {
        super(message);
    }
}

