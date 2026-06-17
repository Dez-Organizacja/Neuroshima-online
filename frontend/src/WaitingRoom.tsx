import { useEffect, useState } from "react";
import Button from "./components/Button";
import { useGameSocketContext } from "./websockets/gameSocketContext";
import DisplayPlayerFactions from "./components/DisplayPlayerFactions";
import { imagesByName } from "./Images";
import { clearCurrentFaction, setCurrentFaction } from "./factionStore";
import "./styles/WaitingRoom.css";

type RoomScreenProps = {
  onSwitchToGame: () => void;
  onSwitchToMenu: () => void;
};



type PlayerFactions = Record<string, string | null>;

type FactionName = "borgo" | "moloch" | "posterunek" | "hegemonia";
type RoomVisibility = "public" | "private";

type FactionDetails = {
  label: string;
  description: string;
};

const factions: Record<FactionName, FactionDetails> = {
  borgo: {
    label: "Borgo",
    description: "Mutants built for direct, overwhelming combat.",
  },
  moloch: {
    label: "Moloch",
    description: "A relentless machine army with strong ranged attacks.",
  },
  posterunek: {
    label: "Posterunek",
    description: "Mobile soldiers who control positioning and initiative.",
  },
  hegemonia: {
    label: "Hegemonia",
    description: "Fast gangs that dominate close-range encounters.",
  },
};

function isRoomVisibility(value: unknown): value is RoomVisibility {
  return value === "public" || value === "private";
}

function isPlayerFactions(value: unknown): value is PlayerFactions {
  return (
    typeof value === "object" &&
    value !== null &&
    !Array.isArray(value) &&
    Object.values(value).every(
      (faction) => typeof faction === "string" || faction === null,
    )
  );
}

export function RoomScreen({
  onSwitchToGame,
  onSwitchToMenu,
}: RoomScreenProps) {
  const {
    latestMessage,
    isConnected,
    setFactionAWFR,
    leaveRoomAWFR,
    startNewGameAWFR,
    setRoomPolicyAWFR,
    getRoomStatusAWFR,
  } = useGameSocketContext();
  const [faction, setFaction] = useState<FactionName | "">("");
  const [playersInRoom, setPlayersInRoom] = useState<string[]>([]);
  const [playerFactions, setPlayerFactions] = useState<PlayerFactions>();
  const [currentReply, setCurrentReply] = useState<string>("");
  const [isSubmittingFaction, setIsSubmittingFaction] = useState(false);
  const [hostUsername, setHostUsername] = useState("");
  const [visibility, setVisibility] = useState<RoomVisibility | "">("");
  const [isUpdatingRoomPolicy, setIsUpdatingRoomPolicy] = useState(false);
  const [pendingHostUsername, setPendingHostUsername] = useState<string | null>(
    null,
  );
  const roomName = localStorage.getItem("room") ?? "Current room";
  const username = localStorage.getItem("username") ?? "Commander";
  const isHost = Boolean(hostUsername && hostUsername === username);
  const selectedFactions = playersInRoom
    .map((player) => playerFactions?.[player])
    .filter((selected): selected is string => typeof selected === "string");

  const canStartGame =
    playersInRoom.length === 2 && selectedFactions.length === 2;

  useEffect(() => {
    if (!latestMessage) {
      return;
    }

    if (
      latestMessage.messageType === "NEWGAME_RESPONSE" &&
      typeof latestMessage.createdGameId === "string"
    ) {
      localStorage.setItem("gameId", latestMessage.createdGameId);
      onSwitchToGame();
    }

    if (
      latestMessage.messageType === "GETROOMSTATUS_RESPONSE" &&
      Array.isArray(latestMessage.playersInRoom) &&
      latestMessage.playersInRoom.every(
        (player) => typeof player === "string",
      ) &&
      isPlayerFactions(latestMessage.playerFactions)
    ) {
      setPlayersInRoom(latestMessage.playersInRoom);
      setPlayerFactions(latestMessage.playerFactions);

      // `factionStore` is module memory, so it is reset by a full page refresh.
      // Restore this player's faction from the server-authoritative room status
      // before switching back to the active game screen.
      const restoredFaction = latestMessage.playerFactions[username];
      if (typeof restoredFaction === "string" && restoredFaction.trim()) {
        setCurrentFaction(restoredFaction);
      }

      const roomPolicy =
        typeof latestMessage.roomPolicy === "object" &&
        latestMessage.roomPolicy !== null
          ? (latestMessage.roomPolicy as Record<string, unknown>)
          : {};
      const reportedHost =
        typeof roomPolicy.host === "string"
          ? roomPolicy.host
          : typeof roomPolicy.hostUsername === "string"
            ? roomPolicy.hostUsername
            : typeof latestMessage.host === "string"
              ? latestMessage.host
              : typeof latestMessage.hostUsername === "string"
                ? latestMessage.hostUsername
                : "";
      const reportedVisibility = isRoomVisibility(roomPolicy.visibility)
        ? roomPolicy.visibility
        : latestMessage.visibility;

      if (reportedHost) {
        setHostUsername(reportedHost);
      }
      if (isRoomVisibility(reportedVisibility)) {
        setVisibility(reportedVisibility);
      }

      const hasActiveGame =
        typeof latestMessage.gameId === "string" &&
        latestMessage.gameId.trim().length > 0 &&
        typeof latestMessage.gameView === "object" &&
        latestMessage.gameView !== null;

      if (hasActiveGame) {
        localStorage.setItem("gameId", latestMessage.gameId as string);
        setCurrentReply("Previous battle session reclaimed.");
        onSwitchToGame();
      } else {
        localStorage.removeItem("gameId");
      }
    }
  }, [latestMessage, onSwitchToGame]);

  useEffect(() => {
    if (!isConnected) {
      return;
    }

    void getRoomStatusAWFR()
      .then((response) => {
        if (response.messageType !== "ERROR") {
          return;
        }

        const authoritativeRoomId = localStorage.getItem("room")?.trim();
        const errorMessage =
          typeof response.error === "string"
            ? response.error
            : "Could not restore the previous room.";

        // useGameSocket synchronises localStorage from the server's
        // CONNECTION envelope before isConnected becomes true. An absent room
        // therefore means the server confirmed that there is no affiliation.
        if (!authoritativeRoomId) {
          localStorage.removeItem("gameId");
          setCurrentReply("The previous room is no longer available.");
          onSwitchToMenu();
          return;
        }

        // Do not strand an affiliated player on the menu because of a
        // temporary room-status failure. Keep the room route and allow the
        // next reconnect/status refresh to recover it.
        setCurrentReply(`${errorMessage} Your room session is still reserved.`);
      })
      .catch((error) => {
        setCurrentReply(
          error instanceof Error
            ? error.message
            : "Could not restore the previous room.",
        );
      });
  }, [getRoomStatusAWFR, isConnected, onSwitchToMenu]);

  async function handleFaction() {
    if (!faction || isSubmittingFaction) {
      return;
    }

    setIsSubmittingFaction(true);
    setCurrentReply("");

    try {
      const response = await setFactionAWFR(faction);

      if (response.messageType === "SETINROOMATTRIBUTES_RESPONSE") {
        if (
          typeof response.faction === "string" &&
          typeof response.serverStatus === "string"
        ) {
          setCurrentReply(response.serverStatus);
          setCurrentFaction(response.faction)
        } else if (typeof response.error === "string") {
          setCurrentReply(response.error);
        }
      } else if (response.messageType === "ERROR") {
        setCurrentReply(
          typeof response.error === "string"
            ? response.error
            : "Could not set faction.",
        );
      }
    } catch (error) {
      setCurrentReply(
        error instanceof Error ? error.message : "Could not set faction.",
      );
    } finally {
      setIsSubmittingFaction(false);
    }
  }
  
  
  async function handleLeave() {
    try {
      const response = await leaveRoomAWFR();
      
      if (response.messageType === "LEAVEROOM_RESPONSE") {
        localStorage.removeItem("room");
        localStorage.removeItem("gameId");
        clearCurrentFaction();
        onSwitchToMenu();
      } else if (response.messageType === "ERROR") {
        setCurrentReply(
          typeof response.error === "string"
          ? response.error
          : "Could not leave room.",
        );
      }
    } catch (error) {
      setCurrentReply(
        error instanceof Error ? error.message : "Could not leave room.",
      );
    }
  }
  
  async function handleStartGame() {
    if (!playerFactions || !canStartGame) {
      setCurrentReply(
        "Two players must select factions before the game can start.",
      );
      return;
    }
    
    try {
      const response = await startNewGameAWFR(playersInRoom, selectedFactions);
      
      if (
        response.messageType === "NEWGAME_RESPONSE" &&
        typeof response.createdGameId === "string"
      ) {
        localStorage.setItem("gameId", response.createdGameId);
        onSwitchToGame();
      } else if (response.messageType === "ERROR") {
        setCurrentReply(
          typeof response.error === "string"
          ? response.error
          : "Could not start game.",
        );
      }
    } catch (error) {
      setCurrentReply(
        error instanceof Error ? error.message : "Could not start game.",
      );
    }
  }
  async function updateRoomPolicy(
    nextVisibility: RoomVisibility,
    nextHostUsername: string,
    successMessage: string,
  ) {
    if (!isHost) {
      setCurrentReply("Only the current host can change the room policy.");
      return;
    }

    if (!nextHostUsername) {
      setCurrentReply("The room host is not available yet.");
      return;
    }

    setIsUpdatingRoomPolicy(true);
    setCurrentReply("");

    try {
      const response = await setRoomPolicyAWFR(
        nextVisibility,
        nextHostUsername,
      );

      if (response.messageType === "SETROOMPOLICY_RESPONSE") {
        if (typeof response.error === "string") {
          setCurrentReply(response.error);
          return;
        }

        const reportedHost =
          typeof response.host === "string"
            ? response.host
            : typeof response.hostUsername === "string"
              ? response.hostUsername
              : nextHostUsername;
        const reportedVisibility = isRoomVisibility(response.visibility)
          ? response.visibility
          : nextVisibility;

        setHostUsername(reportedHost);
        setVisibility(reportedVisibility);
        setCurrentReply(successMessage);
      } else if (response.messageType === "ERROR") {
        setCurrentReply(
          typeof response.error === "string"
            ? response.error
            : "Could not change the room policy.",
        );
      }
    } catch (error) {
      setCurrentReply(
        error instanceof Error
          ? error.message
          : "Could not change the room policy.",
      );
    } finally {
      setIsUpdatingRoomPolicy(false);
      setPendingHostUsername(null);
    }
  }

  function handleVisibilityChange(nextVisibility: RoomVisibility) {
    if (
      nextVisibility === visibility ||
      isUpdatingRoomPolicy ||
      !hostUsername
    ) {
      return;
    }

    void updateRoomPolicy(
      nextVisibility,
      hostUsername,
      `Room visibility changed to ${nextVisibility}.`,
    );
  }

  function handleHostTransfer(nextHostUsername: string) {
    if (
      !visibility ||
      nextHostUsername === hostUsername ||
      isUpdatingRoomPolicy
    ) {
      return;
    }

    setPendingHostUsername(nextHostUsername);
    void updateRoomPolicy(
      visibility,
      nextHostUsername,
      `${nextHostUsername} is now the room host.`,
    );
  }
  
  return (
    <main className="waiting-room">
      <div className="waiting-room__noise" aria-hidden="true" />

      <div className="waiting-room__shell">
        <header className="waiting-room__header">
          <div>
            <p className="waiting-room__eyebrow">Neuroshima Hex</p>
            <h1>Battle staging area</h1>
            <p className="waiting-room__intro">
              Choose your army, confirm your faction, and wait for your
              opponent.
            </p>
          </div>

          <div className="waiting-room__header-actions">
            <div className="room-meta">
              <div className="room-code" title={roomName}>
                <span className="room-code__label">Room</span>
                <strong>{roomName}</strong>
              </div>

              <div
                className={`room-host${isHost ? " is-current-user" : ""}`}
                title={hostUsername || "Host not reported yet"}
              >
                <span className="room-host__mark" aria-hidden="true">
                  ◆
                </span>
                <span className="room-host__content">
                  <span className="room-code__label">Room host</span>
                  <strong>{hostUsername || "Awaiting status…"}</strong>
                  {isHost && <small>You control this room</small>}
                </span>
              </div>
            </div>

            <Button
              className="room-button room-button--ghost"
              text="Leave room"
              onClick={handleLeave}
            />
          </div>
        </header>

        <div className="waiting-room__layout">
          <section className="war-panel war-panel--factions">
            <div className="section-heading">
              <div>
                <p className="section-heading__number">01</p>
                <h2>Select your faction</h2>
              </div>
              <p>Only one commander can claim each army.</p>
            </div>

            <div className="faction-grid">
              {(
                Object.entries(factions) as [FactionName, FactionDetails][]
              ).map(([factionName, details]) => {
                const isSelected = faction === factionName;

                return (
                  <Button
                    key={factionName}
                    className={`faction-card faction-card--${factionName}${
                      isSelected ? " is-selected" : ""
                    }`}
                    onClick={() => {
                      setFaction(factionName);
                      setCurrentReply("");
                    }}
                    ariaPressed={isSelected}
                    text={
                      <>
                        <span className="faction-card__hex">
                          <img
                            src={imagesByName[`${factionName}/sztab`]}
                            alt=""
                          />
                        </span>

                        <span className="faction-card__content">
                          <span className="faction-card__topline">
                            <strong>{details.label}</strong>
                            <span className="faction-card__marker">
                              {isSelected ? "Selected" : "Choose"}
                            </span>
                          </span>
                          <span className="faction-card__description">
                            {details.description}
                          </span>
                        </span>
                      </>
                    }
                  />
                );
              })}
            </div>

            <div className="selection-bar">
              <div className="selection-bar__status">
                <span className="selection-bar__indicator" aria-hidden="true" />
                <div>
                  <span>Current selection</span>
                  <strong>
                    {faction ? factions[faction].label : "No faction selected"}
                  </strong>
                </div>
              </div>

              <Button
                className="room-button room-button--primary"
                text={isSubmittingFaction ? "Confirming…" : "Confirm faction"}
                onClick={handleFaction}
                disabled={!faction || isSubmittingFaction}
              />
            </div>
          </section>

          <aside className="war-panel war-panel--players">
            <div className="section-heading section-heading--compact">
              <div>
                <p className="section-heading__number">02</p>
                <h2>Commanders</h2>
              </div>
              <span className="player-count">
                {playersInRoom.length}
                <small>/2</small>
              </span>
            </div>

            <div className="controlled-player" role="status">
              <span className="controlled-player__mark" aria-hidden="true">
                You
              </span>
              <span className="controlled-player__identity">
                <span>You control this commander</span>
                <strong>{username}</strong>
                <small>
                  Your faction selection and room actions belong to this player.
                </small>
              </span>
            </div>

            <section
              className={`room-policy${isHost ? " is-editable" : ""}`}
              aria-labelledby="room-policy-title"
            >
              <div className="room-policy__heading">
                <div>
                  <span className="room-policy__eyebrow">Room access</span>
                  <strong id="room-policy-title">
                    {visibility
                      ? `${visibility} room`
                      : "Loading room policy…"}
                  </strong>
                </div>
                <span
                  className={`room-policy__lock${isHost ? " is-unlocked" : ""}`}
                  aria-hidden="true"
                >
                  {isHost ? "◆" : "▣"}
                </span>
              </div>

              <div
                className="visibility-switch"
                role="group"
                aria-label="Room visibility"
              >
                {(["public", "private"] as RoomVisibility[]).map(
                  (option) => (
                    <button
                      className={`visibility-switch__option${
                        visibility === option ? " is-active" : ""
                      }`}
                      type="button"
                      key={option}
                      onClick={() => handleVisibilityChange(option)}
                      disabled={
                        !isHost ||
                        !visibility ||
                        isUpdatingRoomPolicy
                      }
                      aria-pressed={visibility === option}
                    >
                      <span aria-hidden="true">
                        {option === "public" ? "◉" : "▣"}
                      </span>
                      {option}
                    </button>
                  ),
                )}
              </div>

              <p className="room-policy__note">
                {isHost
                  ? "You can change access or transfer command from the player list."
                  : `Only ${hostUsername || "the host"} can change room access.`}
              </p>
            </section>

            <DisplayPlayerFactions
              playerFactions={playerFactions ?? {}}
              playersInRoom={playersInRoom}
              currentUsername={username}
              hostUsername={hostUsername}
              canManageRoom={isHost && Boolean(visibility)}
              isRoomPolicyBusy={isUpdatingRoomPolicy}
              pendingHostUsername={pendingHostUsername}
              onMakeHost={handleHostTransfer}
            />

            <div className={`readiness ${canStartGame ? "is-ready" : ""}`}>
              <span className="readiness__icon" aria-hidden="true">
                {canStartGame ? "✓" : "!"}
              </span>
              <div>
                <strong>
                  {canStartGame ? "Battle ready" : "Waiting for players"}
                </strong>
                <p>
                  {canStartGame
                    ? "Both commanders have locked in their factions."
                    : "The match requires two confirmed factions."}
                </p>
              </div>
            </div>

            <Button
              className="room-button room-button--start"
              text="Start game"
              onClick={handleStartGame}
              disabled={!canStartGame}
            />
          </aside>
        </div>

        {currentReply && (
          <div className="room-message" role="status">
            <span aria-hidden="true">◆</span>
            {currentReply}
          </div>
        )}
      </div>
    </main>
  );
}
