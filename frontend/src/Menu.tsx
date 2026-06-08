import { useEffect, useState } from "react";
import Button from "./components/Button";
import TextInput from "./components/TekstInput";
import { imagesByName } from "./Images";
import { useGameSocketContext } from "./websockets/gameSocketContext";
import "./styles/Menu.css";

type MenuScreenProps = {
  onSwitchToWaitingRoom: () => void;
};

type Feedback = {
  message: string;
  tone: "neutral" | "error" | "success";
};

const factionInsignia = ["borgo", "moloch", "posterunek", "hegemonia"];

export default function MenuScreen({
  onSwitchToWaitingRoom,
}: MenuScreenProps) {
  const [joinRoomName, setJoinRoomName] = useState("");
  const [createRoomName, setCreateRoomName] = useState("");
  const [activeRequest, setActiveRequest] = useState<"join" | "create" | null>(
    null,
  );
  const [feedback, setFeedback] = useState<Feedback>({
    message: "Choose an existing room or establish a new battle channel.",
    tone: "neutral",
  });

  const { latestMessage, createRoomAWFR, joinRoomAWFR, isConnected } =
    useGameSocketContext();

  const username = localStorage.getItem("username") ?? "Commander";

  useEffect(() => {
    if (
      latestMessage?.messageType === "CONNECTION" &&
      typeof latestMessage.clientId === "string"
    ) {
      localStorage.setItem("clientID", latestMessage.clientId);
    }
  }, [latestMessage]);

  async function handleJoin() {
    const roomName = joinRoomName.trim();

    if (!roomName || activeRequest) {
      return;
    }

    setActiveRequest("join");
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
              className={`menu-profile__signal${
                isConnected ? " is-online" : ""
              }`}
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
                  <img
                    src={imagesByName[`${factionName}/sztab`]}
                    alt=""
                  />
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
                    placeholder="e.g. OUTPOST-07"
                  />
                  <span className="menu-field__corner" aria-hidden="true" />
                </span>
              </label>

              <Button
                className="menu-action-button menu-action-button--secondary"
                onClick={handleJoin}
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
              <span><b>OR</b></span>
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
                Establish a private staging area and invite another commander.
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
                    placeholder="Name your battle room"
                  />
                  <span className="menu-field__corner" aria-hidden="true" />
                </span>
              </label>

              <Button
                className="menu-action-button menu-action-button--primary"
                onClick={handleCreate}
                disabled={!createRoomName.trim() || activeRequest !== null}
                text={
                  <>
                    <span>
                      {activeRequest === "create"
                        ? "Creating…"
                        : "Create room"}
                    </span>
                    <span aria-hidden="true">+</span>
                  </>
                }
              />
            </article>
          </div>

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