package pl.staszic.neu.game.service;
import pl.staszic.neu.messages.*;
import java.util.Set;

public interface GameService {
    CreateNewRoomResponse createNewRoom(String clientId, CreateNewRoomRequest request);

    JoinRoomResponse joinRoom(String clientId, JoinRoomRequest request);

    LeaveRoomResponse leaveRoom(String clientId, LeaveRoomRequest request);

    GetRoomStatusResponse getRoomStatus(String clientId, GetRoomStatusRequest request);

    SetFactionResponse setFaction(String clientId, SetFactionRequest request);

    NewGameResponse startNewGame(String clientId, NewGameRequest request);

    ActionResponse processAction(String clientId, ActionRequest request);

    EndGameResponse endGame(String clientId, EndGameRequest request);

    void handleClientDisconnect(String clientId);

    void registerClientUsername(String clientId, String username);

    String getAffiliation(String clientId);

    Set<String> getClientIdsInRoom(String roomId);
}
