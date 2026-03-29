package pl.staszic.neu.game.service;

import pl.staszic.neu.messages.*;

public interface GameService {
    CreateNewRoomResponse createNewRoom(String clientId, CreateNewRoomRequest request);

    JoinRoomResponse joinRoom(String clientId, JoinRoomRequest request);

    LeaveRoomResponse leaveRoom(String clientId, LeaveRoomRequest request);

    GetRoomStatusResponse getRoomStatus(String clientId, GetRoomStatusRequest request);

    StartNewGameResponse startNewGame(String clientId, StartNewGameRequest request);

    void processAction(String clientId, ActionRequest request);

    EndGameResponse endGame(String clientId, EndGameRequest request);

    EndTurnResponse endTurn(String clientId, EndTurnRequest request);

    void handleClientDisconnect(String clientId);
}

