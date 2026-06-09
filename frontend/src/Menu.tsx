import { useEffect, useState } from "react";
import Button from "./components/Button";
import TextInput from "./components/TekstInput";
import { imagesByName } from "./Images";
import { useGameSocketContext } from "./websockets/gameSocketContext";
import type { WebSocketMessage } from "./websockets/websocketClient";
import "./styles/Menu.css";

type MenuScreenProps = {
  onSwitchToWaitingRoom: () => void;
};

type Feedback = {
  message: string;
  tone: "neutral" | "error" | "success";
};

type RoomProps = {
  roomId: string;
  membersCount: number;
  host: string;
  visibility: string;
};

const factionInsignia = ["borgo", "moloch", "posterunek", "hegemonia"];

function normaliseRoom(value: unknown): RoomProps | null {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    return null;
  }

  const room = value as Record<string, unknown>;
  const roomId =
    typeof room.roomId === "string"
      ? room.roomId
      : typeof room.id === "string"
        ? room.id
        : null;

  if (!roomId) {
    return null;
  }

  const membersCount =
    typeof room.membersCount === "number"
      ? room.membersCount
      : typeof room.playerCount === "number"
        ? room.playerCount
        : 0;

  const host =
    typeof room.host === "string"
      ? room.host
      : typeof room.hostUsername === "string"
        ? room.hostUsername
        : "Unknown commander";

  return {
    roomId,
    membersCount,
    host,
    visibility:
      typeof room.visibility === "string" ? room.visibility : "public",
  };
}

function extractRoomList(response: WebSocketMessage): RoomProps[] {
  const rawList = Array.isArray(response.roomList)
    ? response.roomList
    : Array.isArray(response.roomsList)
      ? response.roomsList
      : [];

  return rawList
    .map(normaliseRoom)
    .filter((room): room is RoomProps => room !== null)
    .sort((first, second) => first.roomId.localeCompare(second.roomId));
}

export default function MenuScreen({
  onSwitchToWaitingRoom,
}: MenuScreenProps) {
  const [joinRoomName, setJoinRoomName] = useState("");
  const [createRoomName, setCreateRoomName] = useState("");
  const [activeRequest, setActiveRequest] = useState<"join" | "create" | null>(
    null,
  );
  const [joiningRoomId, setJoiningRoomId] = useState<string | null>(null);
  const [isRefreshingRooms, setIsRefreshingRooms] = useState(false);
  const [feedback, setFeedback] = useState<Feedback>({
    message: "Choose an existing room or establish a new battle channel.",
    tone: "neutral",
  });
  const [currentRoomList, setCurrentRoomList] = useState<RoomProps[]>([]);

  const {
    latestMessage,
    createRoomAWFR,
    joinRoomAWFR,
    getRoomListAWFR,
    isConnected,
  } = useGameSocketContext();

  const username = localStorage.getItem("username") ?? "Commander";

  useEffect(() => {
    if (
      latestMessage?.messageType === "CONNECTION" &&
      typeof latestMessage.clientId === "string"
    ) {
      localStorage.setItem("clientID", latestMessage.clientId);
    }
  }, [latestMessage]);

  async function handleRefresh(quiet = false) {
      if (!isConnected || isRefreshingRooms) {
        return;
      }

      setIsRefreshingRooms(true);

      try {
        const response = await getRoomListAWFR();

        if (
          response.messageType === "GETROOMSLIST_RESPONSE" ||
          response.messageType === "GETROOMLIST_RESPONSE"
        ) {
          const rooms = extractRoomList(response);
          setCurrentRoomList(rooms);

          if (!quiet) {
            setFeedback({
              message:
                rooms.length > 0
                  ? `Tactical scan complete. ${rooms.length} open ${rooms.length === 1 ? "room" : "rooms"} found.`
                  : "Tactical scan complete. No public rooms are open.",
              tone: "success",
            });
          }
        } else if (response.messageType === "ERROR") {
          setFeedback({
            message:
              typeof response.error === "string"
                ? response.error
                : "Could not refresh room list.",
            tone: "error",
          });
        }
      } catch (error) {
        setFeedback({
          message:
            error instanceof Error
              ? error.message
              : "Could not refresh room list.",
          tone: "error",
        });
      } finally {
        setIsRefreshingRooms(false);
      }
  }

  useEffect(() => {
    if (isConnected) {
      void handleRefresh(true);
    }
    // Refresh once when the socket becomes available.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isConnected]);

  async function handleJoin(roomNameOverride?: string) {
    const roomName = (roomNameOverride ?? joinRoomName).trim();

    if (!roomName || activeRequest) {
      return;
    }

    setActiveRequest("join");
    setJoiningRoomId(roomName);
    setJoinRoomName(roomName);
    setFeedback({ message: "Contacting room host…", tone: "neutral" });

    try {
      const response = await joinRoomAWFR(roomName);

      if (response.messageType === "JOINROOM_RESPONSE") {
        localStorage.setItem("room", roomName);
        setFeedback({ message: "Room found. Deploying…", tone: "success" });
        onSwitchToWaitingRoom();
      } else if (response.messageType === "ERROR") {
        setFeedback({
          message:
            typeof response.error === "string"
              ? response.error
              : "Could not join that room.",
          tone: "error",
        });
      }
    } catch (error) {
      setFeedback({
        message:
          error instanceof Error ? error.message : "Could not join that room.",
        tone: "error",
      });
    } finally {
      setActiveRequest(null);
      setJoiningRoomId(null);
    }
  }

  async function handleCreate() {
    const roomName = createRoomName.trim();

    if (!roomName || activeRequest) {
      return;
    }

    setActiveRequest("create");
    setFeedback({ message: "Opening a secure battle channel…", tone: "neutral" });

    try {
      const response = await createRoomAWFR(roomName);

      if (response.messageType === "CREATENEWROOM_RESPONSE") {
        localStorage.setItem("room", roomName);
        setFeedback({ message: "Room established. Deploying…", tone: "success" });
        onSwitchToWaitingRoom();
      } else if (response.messageType === "ERROR") {
        setFeedback({
          message:
            typeof response.error === "string"
              ? response.error
              : "Could not create that room.",
          tone: "error",
        });
      }
    } catch (error) {
      setFeedback({
        message:
          error instanceof Error
            ? error.message
            : "Could not create that room.",
        tone: "error",
      });
    } finally {
      setActiveRequest(null);
    }
  }

  return (
    <main className="menu-screen">
      <div className="menu-screen__noise" aria-hidden="true" />
      <div className="menu-screen__grid" aria-hidden="true" />

      <div className="menu-shell">
        <header className="menu-header">
          <div className="menu-brand">
            <div className="menu-brand__mark" aria-hidden="true">
              <span>NH</span>
            </div>

            <div>
              <p className="menu-eyebrow">Neuroshima Hex</p>
              <h1>Command network</h1>
              <p className="menu-header__copy">
                Enter the staging area and prepare your army for deployment.
              </p>
            </div>
          </div>

          <div className="menu-profile">
            <span
              className={`menu-profile__signal${isConnected ? " is-online" : ""}`}
              aria-hidden="true"
            />
            <div>
              <span>{isConnected ? "Network online" : "Connecting"}</span>
              <strong>{username}</strong>
            </div>
          </div>
        </header>

        <section className="menu-console" aria-labelledby="menu-title">
          <div className="menu-console__intro">
            <div>
              <p className="menu-section-number">01 / Deployment</p>
              <h2 id="menu-title">Choose your operation</h2>
            </div>

            <div className="menu-insignia" aria-hidden="true">
              {factionInsignia.map((factionName) => (
                <span className="menu-insignia__hex" key={factionName}>
                  <img src={imagesByName[`${factionName}/sztab`]} alt="" />
                </span>
              ))}
            </div>
          </div>

          <div className="menu-actions">
            <article className="operation-card operation-card--join">
              <div className="operation-card__heading">
                <span className="operation-card__icon" aria-hidden="true">
                  <span>↳</span>
                </span>
                <div>
                  <p>Existing channel</p>
                  <h3>Join a room</h3>
                </div>
              </div>

              <p className="operation-card__description">
                Enter the room identifier supplied by the opposing commander.
              </p>

              <label className="menu-field">
                <span className="menu-field__label">Room identifier</span>
                <span className="menu-field__control">
                  <TextInput
                    className="menu-input"
                    value={joinRoomName}
                    onChange={(value) => {
                      setJoinRoomName(value);
                      if (feedback.tone === "error") {
                        setFeedback({
                          message:
                            "Choose an existing room or establish a new battle channel.",
                          tone: "neutral",
                        });
                      }
                    }}
                    onKeyDown={(event) => {
                      if (event.key === "Enter") {
                        void handleJoin();
                      }
                    }}
                    placeholder="e.g. OUTPOST-07"
                  />
                  <span className="menu-field__corner" aria-hidden="true" />
                </span>
              </label>

              <Button
                className="menu-action-button menu-action-button--secondary"
                onClick={() => void handleJoin()}
                disabled={!joinRoomName.trim() || activeRequest !== null}
                text={
                  <>
                    <span>
                      {activeRequest === "join" ? "Joining…" : "Join room"}
                    </span>
                    <span aria-hidden="true">→</span>
                  </>
                }
              />
            </article>

            <div className="menu-divider" aria-hidden="true">
              <span>
                <b>OR</b>
              </span>
            </div>

            <article className="operation-card operation-card--create">
              <div className="operation-card__heading">
                <span className="operation-card__icon" aria-hidden="true">
                  <span>+</span>
                </span>
                <div>
                  <p>New channel</p>
                  <h3>Create a room</h3>
                </div>
              </div>

              <p className="operation-card__description">
                Establish a staging area and invite another commander.
              </p>

              <label className="menu-field">
                <span className="menu-field__label">New room identifier</span>
                <span className="menu-field__control">
                  <TextInput
                    className="menu-input"
                    value={createRoomName}
                    onChange={(value) => {
                      setCreateRoomName(value);
                      if (feedback.tone === "error") {
                        setFeedback({
                          message:
                            "Choose an existing room or establish a new battle channel.",
                          tone: "neutral",
                        });
                      }
                    }}
                    onKeyDown={(event) => {
                      if (event.key === "Enter") {
                        void handleCreate();
                      }
                    }}
                    placeholder="Name your battle room"
                  />
                  <span className="menu-field__corner" aria-hidden="true" />
                </span>
              </label>

              <Button
                className="menu-action-button menu-action-button--primary"
                onClick={() => void handleCreate()}
                disabled={!createRoomName.trim() || activeRequest !== null}
                text={
                  <>
                    <span>
                      {activeRequest === "create" ? "Creating…" : "Create room"}
                    </span>
                    <span aria-hidden="true">+</span>
                  </>
                }
              />
            </article>
          </div>

          <section className="room-browser" aria-labelledby="room-browser-title">
            <div className="room-browser__header">
              <div>
                <p className="menu-section-number">02 / Tactical scan</p>
                <h2 id="room-browser-title">Open battle channels</h2>
                <p className="room-browser__copy">
                  Public staging rooms detected by the command network.
                </p>
              </div>

              <Button
                className="room-browser__refresh"
                onClick={() => void handleRefresh(false)}
                disabled={!isConnected || isRefreshingRooms}
                text={
                  <>
                    <span
                      className={`room-browser__refresh-icon${isRefreshingRooms ? " is-spinning" : ""}`}
                      aria-hidden="true"
                    >
                      ↻
                    </span>
                    {isRefreshingRooms ? "Scanning…" : "Refresh"}
                  </>
                }
              />
            </div>

            {currentRoomList.length === 0 ? (
              <div className="room-browser__empty">
                <span className="room-browser__empty-hex" aria-hidden="true">
                  ∅
                </span>
                <div>
                  <strong>No public rooms detected</strong>
                  <p>
                    Refresh the tactical scan or establish a new battle channel.
                  </p>
                </div>
              </div>
            ) : (
              <div className="room-browser__grid">
                {currentRoomList.map((room, index) => {
                  const roomIsFull = room.membersCount >= 2;
                  const isJoiningThisRoom = joiningRoomId === room.roomId;

                  return (
                    <article className="room-list-card" key={room.roomId}>
                      <div className="room-list-card__index" aria-hidden="true">
                        {String(index + 1).padStart(2, "0")}
                      </div>

                      <div className="room-list-card__body">
                        <div className="room-list-card__topline">
                          <span className="room-list-card__visibility">
                            <span aria-hidden="true" />
                            {room.visibility}
                          </span>
                          <span
                            className={`room-list-card__capacity${roomIsFull ? " is-full" : ""}`}
                          >
                            {room.membersCount}/2 commanders
                          </span>
                        </div>

                        <h3 title={room.roomId}>{room.roomId}</h3>

                        <div className="room-list-card__host">
                          <span className="room-list-card__host-mark" aria-hidden="true">
                            H
                          </span>
                          <span>
                            <small>Room host</small>
                            <strong>{room.host}</strong>
                          </span>
                        </div>
                      </div>

                      <Button
                        className="room-list-card__join"
                        onClick={() => void handleJoin(room.roomId)}
                        disabled={roomIsFull || activeRequest !== null}
                        text={
                          <>
                            <span>
                              {roomIsFull
                                ? "Room full"
                                : isJoiningThisRoom
                                  ? "Joining…"
                                  : "Join"}
                            </span>
                            {!roomIsFull && <span aria-hidden="true">→</span>}
                          </>
                        }
                      />
                    </article>
                  );
                })}
              </div>
            )}
          </section>

          <div className={`menu-feedback menu-feedback--${feedback.tone}`}>
            <span className="menu-feedback__indicator" aria-hidden="true" />
            <p role={feedback.tone === "error" ? "alert" : "status"}>
              {feedback.message}
            </p>
          </div>
        </section>

        <footer className="menu-footer">
          <span>Encrypted tactical link</span>
          <span className="menu-footer__separator" aria-hidden="true" />
          <span>Two commanders per room</span>
        </footer>
      </div>
    </main>
  );
}
