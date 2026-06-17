package pl.staszic.neu.game.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import pl.staszic.neu.game.clientData.service.ClientDataException;
import pl.staszic.neu.game.clientData.service.ClientDataService;
import pl.staszic.neu.game.clientData.service.model.ClientData;
import pl.staszic.neu.game.model.*;
import pl.staszic.neu.messages.api.*;
import pl.staszic.neu.messages.*;
import pl.staszic.neu.messages.game.*;
import pl.staszic.neu.messages.room.*;
import pl.staszic.neu.rest.service.RestService;
import pl.staszic.neu.security.repo.StoredUser;
import pl.staszic.neu.security.repo.UserRepository;
import pl.staszic.neu.security.repo.repository.UserEntity;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

@Service
public class InMemoryGameService implements GameService {
    private static final Logger logger = LoggerFactory.getLogger(InMemoryGameService.class);

    private final Map<String, Room> activeRooms = new ConcurrentHashMap<>();
    private final Map<String, String> affiliations = new ConcurrentHashMap<>();
    private final Map<String, Game> activeGames = new ConcurrentHashMap<>();

    private final Map<String, ScheduledFuture<?>> pendingDisconnectCleanup =
            new ConcurrentHashMap<>();
    private final Set<String> connectedClients = ConcurrentHashMap.newKeySet();
    private final ScheduledExecutorService disconnectScheduler =
            Executors.newSingleThreadScheduledExecutor(runnable -> {
                Thread thread = new Thread(runnable, "game-reconnect-cleanup");
                thread.setDaemon(true);
                return thread;
            });
    private final long reconnectGraceSeconds;

    private final ClientDataService clientDataService;

    //nwm czy to jest dobre miejsce na restService i url, ale na na razie tak zostanie
    private final RestService restService;
    private final String gameStateServiceUrl;
    private final ObjectMapper objectMapper;
    private final UserRepository userRepository;

    @Autowired
    public InMemoryGameService(
            ClientDataService clientDataService, RestService restService,
            @Value("${game.state-service.url:http://127.0.0.1:5000/api/neuroshima}") String gameStateServiceUrl, ObjectMapper objectMapper,
            UserRepository userRepository,
            @Value("${game.reconnect-grace-seconds:120}") long reconnectGraceSeconds
    ) {
        this.clientDataService = clientDataService;
        this.restService = restService;
        this.gameStateServiceUrl = gameStateServiceUrl;
        this.objectMapper = objectMapper;
        this.userRepository = userRepository;
        this.reconnectGraceSeconds = Math.max(0, reconnectGraceSeconds);
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
        response.setServerStatus("STARTED room=" + request.getRoomId() + " player=" + clientDataService.getClientData(clientId).getUsername());
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
        response.setRoomId(room.getRoomId());
        response.setClientId(clientId);
        response.setServerStatus("JOINED room=" + request.getRoomId() + " player=" + clientDataService.getUsernameBySessionId(clientId));
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
        response.setServerStatus("LEFT room=" + request.getRoomId() + " player=" + clientDataService.getUsernameBySessionId(clientId));
        return response;
    }

    @Override
    public KickFromRoomResponse kickFromRoom(String clientId, KickFromRoomRequest request) {
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

        if(!room.getRoomPolicy().getHost().equals(clientId)){
            throw new GameValidationException("Only host can kick players from the room");
        }

        if(room.hasActiveGame()){
            throw new GameValidationException("Cannot kick players: game already started in room=" + request.getRoomId());
        }

        String kickedPlayer = null;
        try {
            kickedPlayer = clientDataService.findSessionIdByUsername(request.getKickedPlayerUsername());
        }
        catch (ClientDataException e){
            throw new GameValidationException("No player with username=" + request.getKickedPlayerUsername() + " found");
        }

        if(!room.hasPlayer(kickedPlayer)){
            throw new GameValidationException("Player with username=" + request.getKickedPlayerUsername() + " is not a member of room=" + request.getRoomId());
        }

        try {
            room.removePlayer(kickedPlayer);
            affiliations.remove(kickedPlayer);
            if(room.isEmpty()){
                activeRooms.remove(request.getRoomId());
            }
        } catch (Exception e) {
            throw new GameValidationException(e.getMessage());
        }

        KickFromRoomResponse response = new KickFromRoomResponse();
        response.setClientId(clientId);
        response.setKickerUsername(clientDataService.getUsernameBySessionIdOrDefault(clientId, "Unknown"));
        response.setServerStatus("KICKED from room=" + request.getRoomId() + " player=" + request.getKickedPlayerUsername());
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

        String affiliatedRoomId = affiliations.get(clientId);
        if (!request.getRoomId().equals(affiliatedRoomId) || !room.hasPlayer(clientId)) {
            throw new GameValidationException("Client is not a member of this room");
        }

        Set<String> playerNamesInRoom = new HashSet<>();
        Map<String, String> playerFactionsByUsername = new LinkedHashMap<>();
        Map<String, String> playerFactionsByClientId = room.getAllPlayerFactions();

        for (String id : room.getPlayerIds()) {
            String username = clientDataService.getUsernameBySessionId(id);
            playerNamesInRoom.add(username);

            String faction = playerFactionsByClientId.get(id);
            playerFactionsByUsername.put(username, faction);
        }

        GetRoomStatusResponse response = new GetRoomStatusResponse();
        response.setClientId(clientId);
        response.setRoomId(request.getRoomId());
        response.setGameId(room.getGameId());

        if (room.hasActiveGame()) {
            Game activeGame = activeGames.get(room.getGameId());
            if (activeGame != null && activeGame.getGameState() != null) {
                response.setGameView(buildGameView(activeGame.getGameState()));
            }
        }

        RoomPolicyView roomPolicyView = new RoomPolicyView();
        try {
            roomPolicyView.setHostUsername(clientDataService.getUsernameBySessionIdOrDefault(room.getRoomPolicy().getHost(), "Unknown"));
        }
        catch (Exception e){
            logger.error("Error getting host username for roomId={}: {}", request.getRoomId(), e.getMessage());
            roomPolicyView.setHostUsername("Unknown");
        }
        roomPolicyView.setVisibility(room.getRoomPolicy().getVisibility());
        response.setRoomPolicyView(roomPolicyView);

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

        response.setRoomId(room.getRoomId());
        response.setStatus(status);
        response.setFaction(faction);
        response.setServerStatus("Attributes successfully changed in room=" + roomId);
        return response;
    }

    @Override
    public SetRoomPolicyResponse setRoomPolicy(String clientId, SetRoomPolicyRequest request) {
        request.setClientId(clientId);

        SetRoomPolicyResponse response = new SetRoomPolicyResponse();
        response.setClientId(clientId);

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

        RoomPolicy newPolicy = null;
        try {
            newPolicy = new RoomPolicy(request.getVisibility(), clientDataService.findSessionIdByUsername(request.getHostUsername()));
        }
        catch (ClientDataException e){
            response.setError("Error setting room policy: " + e.getMessage());
            return response;
        }

        synchronized (room) {
            if (!room.hasPlayer(clientId)) {
                response.setError("Client is not a member of room=" + roomId);
                return response;
            }
            if (!clientDataService.getUsernameBySessionId(clientId).equals(clientDataService.getUsernameBySessionId(room.getRoomPolicy().getHost()))) {
                response.setError("Only the host can change the room policy");
                return response;
            }

            room.mergeRoomPolicy(newPolicy);
        }

        response.setHostUsername(clientDataService.getUsernameBySessionIdOrDefault(room.getRoomPolicy().getHost(), "Unknown"));
        response.setVisibility(room.getRoomPolicy().getVisibility());
        response.setServerStatus("Room policy successfully changed in room=" + roomId);
        return response;
    }

    public GetRoomsListResponse getRoomsList(String clientId, GetRoomsListRequest request){
        request.setClientId(clientId);

        GetRoomsListResponse response = new GetRoomsListResponse();
        response.setClientId(clientId);

        Set<RoomBrowserView> roomsList = new HashSet<>();

        synchronized (activeRooms) {
            for (Room room : activeRooms.values()) {
                if (room.hasActiveGame()) {
                    continue;
                }
                if (room.getRoomPolicy().getVisibility() == RoomPolicy.Visibility.PRIVATE) {
                    continue;
                }

                RoomBrowserView roomBrowserView = new RoomBrowserView();
                roomBrowserView.setRoomId(room.getRoomId());
                roomBrowserView.setMembersCount(room.getRoomSize());
                roomBrowserView.setVisibility(room.getRoomPolicy().getVisibility());
                roomBrowserView.setHostUsername(clientDataService.getUsernameBySessionIdOrDefault(room.getRoomPolicy().getHost(), "Unknown"));

                roomsList.add(roomBrowserView);
            }
        }

        response.setRoomsList(roomsList);
        response.setServerStatus("Rooms list generated by clientId: " + clientId);

        return response;

    }

    @Override
    public GetUserDataResponse getUserData(String clientId, GetUserDataRequest request){
        request.setClientId(clientId);

        GetUserDataResponse response = new GetUserDataResponse();

        String username;
        try {
            username = clientDataService.findSessionIdByUsername(clientId);
        }        catch (ClientDataException e){
            response.setError("No user data found for clientId=" + clientId);
            return response;
        }

        StoredUser entity = userRepository.findByUsername(username).orElse(null);
        if(entity == null){
            response.setError("No user data found for username=" + username);
            return response;
        }

        response.setUsername(username);
        response.setMatches(entity.matches());
        response.setWins(entity.wins());
        response.setServerStatus("User data retrieved for username=" + username);

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
        if(!clientId.equals(room.getRoomPolicy().getHost())){
            throw new GameValidationException("Only host can start new game.");
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
        if(game.getCurrentFaction() != null) {
            String playerFaction = game.getPlayerFaction(clientId);
            if (playerFaction == null) {
                throw new GameValidationException("Client is not a player in the game");
            }
            if (!playerFaction.equals(game.getCurrentFaction())) {
                throw new GameValidationException("It's not the player's turn");
            }
        }
        else{
            logger.warn("Current faction in game is not defined, clientId={}, gameId={}, gameState={}", clientId, request.getGameId(), game.getGameState());
        }

        GameStatusChangeRequest gameStatusChangeRequest = new GameStatusChangeRequest();
        gameStatusChangeRequest.setGameState(game.getGameState());
        gameStatusChangeRequest.setUserAction(request.getActionData());

        JsonNode responseGameDataJsonMessage = restService.postJson(gameStateServiceUrl + "/action", objectMapper.valueToTree(gameStatusChangeRequest));

        GameStatusChangeResponse responseGameData = objectMapper.convertValue(responseGameDataJsonMessage, GameStatusChangeResponse.class);
        game.setGameState(responseGameData.getGameState());

        // A game in the gameover phase remains available long enough for every
        // client to render the scoreboard. It is removed only after a player
        // explicitly sends ENDGAME_REQUEST from that scoreboard.

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
        if (!affiliations.containsKey(clientId)) {
            throw new GameValidationException("Client is not in a room");
        }

        Room room = activeRooms.get(affiliations.get(clientId));
        if (room == null || !room.hasPlayer(clientId)) {
            throw new GameValidationException("Client is not in a room");
        }

        synchronized (room) {
            // ENDGAME_REQUEST is intentionally idempotent. If both players press
            // a scoreboard button at nearly the same time, the second request
            // still succeeds without recording the match twice.
            if (!room.hasActiveGame()) {
                return createEndGameResponse(clientId, request.getGameId());
            }

            if (!request.getGameId().equals(room.getGameId())) {
                throw new GameValidationException(
                        "Client is not affiliated with gameId=" + request.getGameId()
                );
            }

            Game game = activeGames.get(request.getGameId());
            if (game == null) {
                room.clearGame();
                return createEndGameResponse(clientId, request.getGameId());
            }

            JsonNode phaseNode = game.getGameState() == null
                    ? null
                    : game.getGameState().path("state").path("phase");
            if (phaseNode == null || !phaseNode.isTextual()
                    || !"gameover".equalsIgnoreCase(phaseNode.asText())) {
                throw new GameValidationException(
                        "Cannot end game before it reaches phase=gameover"
                );
            }

            try {
                JsonNode winnerNode = game.getGameState().get("winner");
                String winner = (winnerNode == null || winnerNode.isNull())
                        ? null
                        : winnerNode.asText();

                if (winner == null) {
                    logger.warn("Game game={} ended with no winner", request.getGameId());
                } else {
                    logger.info(
                            "Game game={} ended with winner={}",
                            request.getGameId(),
                            winner
                    );
                }

                for (Map.Entry<String, String> entry
                        : room.getActivePlayerFactions().entrySet()) {
                    String playerId = entry.getKey();
                    String playerFaction = entry.getValue();

                    String username = clientDataService
                            .getUsernameBySessionIdOrDefault(playerId, null);
                    if (username == null) {
                        logger.warn(
                                "Cannot resolve username for playerId={}, skipping stats update",
                                playerId
                        );
                        continue;
                    }

                    boolean won = winner != null && playerFaction.equals(winner);
                    if (won) {
                        logger.info(
                                "Player playerId={} username={} wins the game",
                                playerId,
                                username
                        );
                    }

                    try {
                        userRepository.recordMatch(username, won);
                    } catch (Exception e) {
                        logger.warn(
                                "Failed to update stats for username={}: {}",
                                username,
                                e.getMessage()
                        );
                    }
                }
            } catch (Exception e) {
                throw new GameValidationException(
                        "Game data has no winner: " + e.getMessage()
                );
            }

            room.clearGame();
            activeGames.remove(request.getGameId());
            return createEndGameResponse(clientId, request.getGameId());
        }
    }

    private EndGameResponse createEndGameResponse(String clientId, String gameId) {
        EndGameResponse response = new EndGameResponse();
        response.setClientId(clientId);
        response.setGameId(gameId);
        return response;
    }


    @Override
    public void handleClientDisconnect(String clientId) {
        connectedClients.remove(clientId);

        ScheduledFuture<?> previousCleanup = pendingDisconnectCleanup.remove(clientId);
        if (previousCleanup != null) {
            previousCleanup.cancel(false);
        }

        Runnable cleanup = () -> {
            pendingDisconnectCleanup.remove(clientId);
            removeDisconnectedClient(clientId);
        };

        if (reconnectGraceSeconds == 0) {
            cleanup.run();
            return;
        }

        ScheduledFuture<?> cleanupFuture = disconnectScheduler.schedule(
                cleanup,
                reconnectGraceSeconds,
                TimeUnit.SECONDS
        );
        pendingDisconnectCleanup.put(clientId, cleanupFuture);

        logger.info(
                "Client {} disconnected; preserving room/game state for {} seconds",
                clientId,
                reconnectGraceSeconds
        );
    }

    private void removeDisconnectedClient(String clientId) {
        if (connectedClients.contains(clientId)) {
            logger.info(
                    "Skipping disconnect cleanup for client {} because it reconnected",
                    clientId
            );
            return;
        }

        clientDataService.removeClientData(clientId);
        String roomId = affiliations.remove(clientId);
        if (roomId == null) {
            return;
        }

        Room room = activeRooms.get(roomId);
        if (room == null) {
            return;
        }

        synchronized (room) {
            try {
                room.removePlayer(clientId);
            } catch (Exception ignored) {
                // The player may already have left through an explicit request.
            }

            if (room.hasActiveGame()) {
                activeGames.remove(room.getGameId());
                room.clearGame();
            }

            if (room.isEmpty()) {
                activeRooms.remove(roomId);
            }
        }

        logger.info(
                "Reconnect grace period expired for client {}; removed from room {}",
                clientId,
                roomId
        );
    }

    @Override
    public void registerClientUsername(String clientId, String username) {
        connectedClients.add(clientId);

        ScheduledFuture<?> pendingCleanup = pendingDisconnectCleanup.remove(clientId);
        if (pendingCleanup != null) {
            pendingCleanup.cancel(false);
            logger.info("Client {} reclaimed the existing session", clientId);
        }

        clientDataService.addClientData(clientId, new ClientData(username));
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
    private static boolean isBlank(String value) {
        return value == null || value.trim().isEmpty();
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