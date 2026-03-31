package pl.staszic.neu.game.service;

import com.fasterxml.jackson.databind.JsonNode;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import pl.staszic.neu.game.model.Room;
import pl.staszic.neu.game.model.Game;
import pl.staszic.neu.messages.*;
import pl.staszic.neu.rest.service.RestService;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class InMemoryGameService implements GameService {
    private static final Logger logger = LoggerFactory.getLogger(InMemoryGameService.class);

    private final Map<String, Room> activeRooms = new ConcurrentHashMap<>();
    private final Map<String, String> affiliations = new ConcurrentHashMap<>();
    private final Map<String, Game> activeGames = new ConcurrentHashMap<>();

    //nwm czy to jest dobre miejsce na restService i url, ale na na razie tak zostanie
    private final RestService restService;
    private final String gameStateServiceUrl;

    @Autowired
    public InMemoryGameService(
        RestService restService,
        @Value("${game.state-service.url:http://127.0.0.1:5000/api/neuroshima}") String gameStateServiceUrl
    ) {
        this.restService = restService;
        this.gameStateServiceUrl = gameStateServiceUrl;
    }
    //koniec slabego kodu

    @Override
    public CreateNewRoomResponse createNewRoom(String clientId, CreateNewRoomRequest request) {
        request.setClientId(clientId);

        if (isBlank(request.getRoomId())) {
            throw new GameValidationException("Room id is null or empty");
        }
        if (activeRooms.containsKey(request.getRoomId())) {
            throw new GameValidationException("Room already exists");
        }
        if (affiliations.containsKey(clientId)) {
            throw new GameValidationException("Client is already in a room");
        }

        String roomId = request.getRoomId();
        Room room = new Room(roomId);
        try {
            room.addPlayer(clientId);
            affiliations.put(clientId, roomId);
        } catch (Exception e) {
            throw new GameValidationException(e.getMessage());
        }
        activeRooms.put(roomId, room);

        CreateNewRoomResponse response = new CreateNewRoomResponse();
        response.setClientId(clientId);
        response.setCreatedRoomId(roomId);
        response.setServerStatus("STARTED room=" + request.getRoomId() + " player=" + request.getPlayerName());
        return response;
    }

    @Override
    public JoinRoomResponse joinRoom(String clientId, JoinRoomRequest request) {
        request.setClientId(clientId);

        if (isBlank(request.getRoomId())) {
            throw new GameValidationException("Room id is null or empty");
        }
        if (affiliations.containsKey(clientId)) {
            throw new GameValidationException("Client is already in a room");
        }

        Room room = activeRooms.get(request.getRoomId());
        if (room == null) {
            throw new GameValidationException("Room does not exist");
        }

        try {
            room.addPlayer(request.getClientId());
            affiliations.put(clientId, request.getRoomId());
        } catch (Exception e) {
            throw new GameValidationException(e.getMessage());
        }

        JoinRoomResponse response = new JoinRoomResponse();
        response.setClientId(clientId);
        response.setServerStatus("JOINED room=" + request.getRoomId() + " player=" + request.getPlayerName());
        return response;
    }

    @Override
    public LeaveRoomResponse leaveRoom(String clientId, LeaveRoomRequest request) {
        request.setClientId(clientId);

        if (!affiliations.containsKey(clientId)) {
            throw new GameValidationException("Client is not in a room");
        }
        if (isBlank(request.getRoomId())) {
            throw new GameValidationException("Room id is null or empty");
        }

        Room room = activeRooms.get(request.getRoomId());
        if (room == null) {
            throw new GameValidationException("Room does not exist");
        }

        try {
            room.removePlayer(clientId);
            affiliations.remove(clientId);
            if (room.hasActiveGame()) {
                activeGames.remove(room.getGameId());
                room.clearGame();
            }
        } catch (Exception e) {
            throw new GameValidationException(e.getMessage());
        }

        LeaveRoomResponse response = new LeaveRoomResponse();
        response.setClientId(clientId);
        response.setServerStatus("LEFT room=" + request.getRoomId() + " player=" + request.getPlayerName());
        return response;
    }

    @Override
    public GetRoomStatusResponse getRoomStatus(String clientId, GetRoomStatusRequest request) {
        request.setClientId(clientId);

        if (isBlank(request.getRoomId())) {
            throw new GameValidationException("Room id is null or empty");
        }

        Room room = activeRooms.get(request.getRoomId());
        if (room == null) {
            throw new GameValidationException("Room does not exist");
        }

        GetRoomStatusResponse response = new GetRoomStatusResponse();
        response.setClientId(clientId);
        response.setRoomId(request.getRoomId());
        response.setGameId(room.getGameId());
        response.setPlayersInRoom(room.getPlayerIds());
        response.setServerStatus("STATUS for room=" + request.getRoomId() + ": players=" + room.getPlayerIds() + " activeGame=" + room.hasActiveGame());
        return response;
    }

    @Override
    public NewGameResponse startNewGame(String clientId, NewGameRequest request) {
        request.setClientId(clientId);

        if (isBlank(request.getRoomId())) {
            throw new GameValidationException("STARTNEWGAME_REQUEST requires roomId");
        }



        //dodaj sprawdzenie poprawnosci scenario

        String affiliatedRoomId = affiliations.get(clientId);
        if (affiliatedRoomId == null) {
            throw new GameValidationException("Client is not in a room");
        }
        if (!request.getRoomId().equals(affiliatedRoomId)) {
            throw new GameValidationException("Client is not affiliated with roomId=" + request.getRoomId());
        }

        Room room = activeRooms.get(request.getRoomId());
        if (room == null) {
            throw new GameValidationException("Room does not exist");
        }
        if (!room.hasPlayer(clientId)) {
            throw new GameValidationException("Client is not a member of room=" + request.getRoomId());
        }
        if (room.hasActiveGame()) {
            throw new GameValidationException("Room already has active game: " + room.getGameId());
        }

        Game game = new Game();
        game.setGameState(restService.postJson(gameStateServiceUrl+"/newgame", request.getScenario()));
        activeGames.put(game.getGameId(), game);

        room.setGameId(game.getGameId());

        NewGameResponse response = new NewGameResponse();
        response.setClientId(clientId);
        response.setRoomId(request.getRoomId());
        response.setCreatedGameId(game.getGameId());
        response.setServerStatus("STARTED game=" + request.getRoomId() + " in room=" + response.getRoomId() + " by=" + clientId);
        return response;
    }

    @Override
    public void processAction(String clientId, ActionRequest request) {
        request.setClientId(clientId);

        if (isBlank(request.getGameId())) {
            throw new GameValidationException("ACTION_REQUEST requires gameId");
        }
        if (!activeGames.containsKey(request.getGameId())) {
            throw new GameValidationException("Unknown gameId: " + request.getGameId());
        }

        logger.info("Action processed: {}", request);
    }

    @Override
    public EndGameResponse endGame(String clientId, EndGameRequest request) { //do zrobienia
//        request.setClientId(clientId);
//
//        if (isBlank(request.getGameId())) {
//            throw new GameValidationException("ENDGAME_REQUEST requires gameId");
//        }
//        if (!activeGames.containsKey(request.getGameId())) {
//            throw new GameValidationException("Unknown gameId: " + request.getGameId());
//        }
//
//        String roomId = activeGames.remove(game.getGameId());
//        if (roomId != null) {
//            Room room = activeRooms.get(roomId);
//            if (room != null && request.getGameId().equals(room.getGameId())) {
//                room.clearGame();
//            }
//        }
//
        EndGameResponse response = new EndGameResponse();
//        response.setClientId(clientId);
//        response.setGameId(request.getGameId());
//        response.setEnded(true);
//        response.setSummary("Game ended. Winner=" + request.getWinnerId() + ", reason=" + request.getReason());
        return response;
    }


    @Override
    public void handleClientDisconnect(String clientId) {
        String roomId = affiliations.remove(clientId);
        if (roomId == null) {
            return;
        }

        Room room = activeRooms.get(roomId);
        if (room == null) {
            return;
        }

        try {
            room.removePlayer(clientId);
        } catch (Exception ignored) {
            // Klient mogl zostac usuniety z pokoju przez inny przeplyw.
        }

        if (room.hasActiveGame()) {
            activeGames.remove(room.getGameId());
            room.clearGame();
        }
    }

    private boolean isBlank(String value) {
        return value == null || value.isBlank();
    }
}


