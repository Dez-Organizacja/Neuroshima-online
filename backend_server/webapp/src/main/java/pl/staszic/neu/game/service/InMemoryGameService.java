package pl.staszic.neu.game.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import pl.staszic.neu.game.model.RoomMember;
import pl.staszic.neu.game.model.RoomPropertiesView;
import pl.staszic.neu.messages.GameStatusChangeRequest;
import pl.staszic.neu.game.model.Room;
import pl.staszic.neu.game.model.Game;
import pl.staszic.neu.messages.*;
import pl.staszic.neu.rest.service.RestService;

import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

import static org.apache.logging.log4j.util.Strings.isBlank;

@Service
public class InMemoryGameService implements GameService {
    private static final Logger logger = LoggerFactory.getLogger(InMemoryGameService.class);

    private final Map<String, Room> activeRooms = new ConcurrentHashMap<>();
    private final Map<String, String> affiliations = new ConcurrentHashMap<>();
    private final Map<String, Game> activeGames = new ConcurrentHashMap<>();
    private final Map<String, String> clientUsernames = new ConcurrentHashMap<>();

    //nwm czy to jest dobre miejsce na restService i url, ale na na razie tak zostanie
    private final RestService restService;
    private final String gameStateServiceUrl;
    private final ObjectMapper objectMapper;

    @Autowired
    public InMemoryGameService(
            RestService restService,
            @Value("${game.state-service.url:http://127.0.0.1:5000/api/neuroshima}") String gameStateServiceUrl, ObjectMapper objectMapper
    ) {
        this.restService = restService;
        this.gameStateServiceUrl = gameStateServiceUrl;
        this.objectMapper = objectMapper;
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
        response.setServerStatus("STARTED room=" + request.getRoomId() + " player=" + clientUsernames.get(clientId));
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
        response.setServerStatus("JOINED room=" + request.getRoomId() + " player=" + clientUsernames.get(clientId));
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
            if(room.isEmpty()){
                activeRooms.remove(request.getRoomId());
            }
        } catch (Exception e) {
            throw new GameValidationException(e.getMessage());
        }

        LeaveRoomResponse response = new LeaveRoomResponse();
        response.setClientId(clientId);
        response.setServerStatus("LEFT room=" + request.getRoomId() + " player=" + clientUsernames.get(clientId));
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

        Set<String> playerNamesInRoom = new HashSet<>();
        Map<String, String> playerFactionsByUsername = new LinkedHashMap<>();
        Map<String, String> playerFactionsByClientId = room.getAllPlayerFactions();

        for (String id : room.getPlayerIds()) {
            String username = clientUsernames.getOrDefault(id, "Unknown");
            playerNamesInRoom.add(username);

            String faction = playerFactionsByClientId.get(id);
            playerFactionsByUsername.put(username, faction);
        }

        GetRoomStatusResponse response = new GetRoomStatusResponse();
        response.setClientId(clientId);
        response.setRoomId(request.getRoomId());
        response.setGameId(room.getGameId());

        RoomPropertiesView roomPropertiesView = new RoomPropertiesView();
        roomPropertiesView.setHostUsername(clientUsernames.getOrDefault(room.getRoomProperties().getHost(), "Unknown"));
        roomPropertiesView.setVisibility(room.getRoomProperties().getVisibility());
        response.setRoomPropertiesView(roomPropertiesView);

        response.setPlayersInRoom(playerNamesInRoom);
        response.setPlayerFactions(playerFactionsByUsername);
        response.setServerStatus("STATUS for room=" + request.getRoomId() + ": players=" + room.getPlayerIds() + " playerFactions=" + playerFactionsByUsername + " activeGame=" + room.hasActiveGame());
        return response;
    }

    @Override
    public SetInRoomAttributesResponse setInRoomAttributes(String clientId, SetInRoomAttributesRequest request) {
        request.setClientId(clientId);

        SetInRoomAttributesResponse response = new SetInRoomAttributesResponse();
        response.setClientId(clientId);

        String faction = request.getFaction();
        RoomMember.Status status = request.getStatus();

        if (isBlank(faction)) {
            response.setError("Faction is null or empty");
            return response;
        }

        faction = faction.trim();
        String roomId = affiliations.get(clientId);

        if (roomId == null) {
            response.setError("Client is not in a room");
            return response;
        }

        Room room = activeRooms.get(roomId);
        if (room == null) {
            response.setError("Room does not exist");
            return response;
        }

        if(room.hasActiveGame()) {
            response.setError("Cannot change faction: game already started in room=" + roomId);
            return response;
        }

        RoomMember newRoomMember = new RoomMember();
        newRoomMember.setClientId(clientId);
        newRoomMember.setFaction(faction);
        newRoomMember.setStatus(status);

        synchronized (room) {
            if (!room.hasPlayer(clientId)) {
                response.setError("Client is not a member of room=" + roomId);
                return response;
            }

            room.mergePlayerAttributes(clientId, newRoomMember);
        }

        response.setStatus(status);
        response.setFaction(faction);
        response.setServerStatus("Attributes successfully changed in room=" + roomId);
        return response;
    }

    @Override
    public NewGameResponse startNewGame(String clientId, NewGameRequest request) {
        request.setClientId(clientId);

        if (isBlank(request.getRoomId())) {
            throw new GameValidationException("STARTNEWGAME_REQUEST requires roomId");
        }


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

        ApiNewGameRequest apiNewGameRequest = new ApiNewGameRequest();
        JsonNode scenarioNode;
        try {
            scenarioNode = objectMapper.valueToTree(room.getFactions());
        } catch (IllegalStateException e) {
            throw new GameValidationException("Cannot start game: " + e.getMessage());
        }

        game.setPlayerFactions(room.getActivePlayerFactions());
        apiNewGameRequest.setScenario(scenarioNode);

        game.setGameState(restService.postJson(gameStateServiceUrl, objectMapper.valueToTree(apiNewGameRequest)));
        activeGames.put(game.getGameId(), game);

        room.setGameId(game.getGameId());

        NewGameResponse response = new NewGameResponse();
        response.setClientId(clientId);
        response.setRoomId(request.getRoomId());
        response.setCreatedGameId(game.getGameId());
        response.setGameView(buildGameView(game.getGameState()));
        response.setServerStatus("STARTED game=" + request.getRoomId() + " in room=" + response.getRoomId() + " by=" + clientId);
        return response;
    }

    private JsonNode buildGameView(JsonNode gameState) {
        GameViewRequest gameViewRequest = new GameViewRequest();
        gameViewRequest.setGameState(gameState);

        JsonNode responseGameViewJsonMessage = restService.postJson(
                gameStateServiceUrl + "/view",
                objectMapper.valueToTree(gameViewRequest)
        );
        GameViewResponse gameViewResponse = objectMapper.convertValue(responseGameViewJsonMessage, GameViewResponse.class);
        return gameViewResponse.getGameView();
    }

    @Override
    public ActionResponse processAction(String clientId, ActionRequest request) {
        request.setClientId(clientId);

        if (isBlank(request.getGameId())) {
            throw new GameValidationException("ACTION_REQUEST requires gameId");
        }
        if (!activeGames.containsKey(request.getGameId())) {
            throw new GameValidationException("Unknown gameId: " + request.getGameId());
        }

        Game game = activeGames.get(request.getGameId());

        //odkomentowac to na produkcji, ale na razie niech bedzie latwiej testowac
//        if(game.getCurrentFaction() != null) {
//            String playerFaction = game.getPlayerFaction(clientId);
//            if (playerFaction == null) {
//                throw new GameValidationException("Client is not a player in the game");
//            }
//            if (!playerFaction.equals(game.getCurrentFaction())) {
//                throw new GameValidationException("It's not the player's turn");
//            }
//        }
//        else{
//            logger.warn("Current faction in game is not defined, clientId={}, gameId={}, gameState={}", clientId, request.getGameId(), game.getGameState());
//        }

        GameStatusChangeRequest gameStatusChangeRequest = new GameStatusChangeRequest();
        gameStatusChangeRequest.setGameState(game.getGameState());
        gameStatusChangeRequest.setUserAction(request.getActionData());

        JsonNode responseGameDataJsonMessage = restService.postJson(gameStateServiceUrl + "/action", objectMapper.valueToTree(gameStatusChangeRequest));

        GameStatusChangeResponse responseGameData = objectMapper.convertValue(responseGameDataJsonMessage, GameStatusChangeResponse.class);
        game.setGameState(responseGameData.getGameState());

        ActionResponse response = new ActionResponse();
        response.setGameView(buildGameView(game.getGameState()));

        logger.info("Action processed: {}", request);

        return response;
    }

    @Override
    public EndGameResponse endGame(String clientId, EndGameRequest request) {
        request.setClientId(clientId);

        if (isBlank(request.getGameId())) {
            throw new GameValidationException("ENDGAME_REQUEST requires gameId");
        }
        if (!activeGames.containsKey(request.getGameId())) {
            throw new GameValidationException("Unknown gameId: " + request.getGameId());
        }
        if(!affiliations.containsKey(clientId)){
            throw new GameValidationException("Client is not in a room");
        }
        Room room = activeRooms.get(affiliations.get(clientId));

        if(room.getGameId() != null && !request.getGameId().equals(room.getGameId())){
            throw new GameValidationException("Client is not affiliated with gameId=" + request.getGameId());
        }

        room.clearGame();

        activeGames.remove(request.getGameId());

        EndGameResponse response = new EndGameResponse();
        response.setClientId(clientId);
        response.setGameId(request.getGameId());
        return response;
    }


    @Override
    public void handleClientDisconnect(String clientId) {
        clientUsernames.remove(clientId);
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

        if(room.isEmpty()){
            activeRooms.remove(roomId);
        }
    }

    private boolean isBlank(String value) {
        return value == null || value.isBlank();
    }

    @Override
    public void registerClientUsername(String clientId, String username) {
        clientUsernames.put(clientId, username);
    }

    @Override
    public String getAffiliation(String clientId) {
        try{
            return affiliations.get(clientId);
        }        catch (Exception e){
            logger.error("Error getting affiliation for clientId={}: {}", clientId, e.getMessage());
            return null;
        }
    }
    @Override
    public Set<String> getClientIdsInRoom(String roomId) {
        Room room = activeRooms.get(roomId);

        if (room == null) {
            return Set.of();
        }

        return room.getPlayerIds();
    }
}
