package pl.staszic.neu.game.event;

/**
 * Publikowane za każdym razem, gdy gra zostaje usunięta z pokoju
 * (zakończenie gry, wyjście gracza, rozłączenie). Nasłuchiwane przez
 * warstwę WebSocket, która rozsyła powiadomienie do graczy w pokoju.
 */
public record GameRemovedFromRoomEvent(String roomId, String gameId) { }
