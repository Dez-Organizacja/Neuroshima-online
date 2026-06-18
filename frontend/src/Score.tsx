import { useEffect, useMemo, useRef, useState } from "react";
import type { GameState } from "./Dlaigora";
import Button from "./components/Button";
import { imagesByName } from "./Images";
import { useGameSocketContext } from "./websockets/gameSocketContext";
import type { WebSocketMessage } from "./websockets/websocketClient";
import "./styles/Score.css";

type ScoreBoardProps = {
  gameView: GameState["view"];
  onSwitchToWaitingRoom: () => void;
  onSwitchToMenu: () => void;
};

type FactionResult = {
  name: string;
  hp: number;
  isWinner: boolean;
};

type NavigationTarget = "room" | "menu" | null;

function normalize(value: string): string {
  return value.trim().toLocaleLowerCase();
}

function toLabel(value: string): string {
  if (!value) {
    return "Unknown";
  }

  return value
    .replace(/[_-]+/g, " ")
    .replace(/\b\w/g, (letter) => letter.toLocaleUpperCase());
}

function findMatchingKey<T>(
  record: Record<string, T>,
  key: string,
): string | undefined {
  const normalizedKey = normalize(key);

  return Object.keys(record).find(
    (recordKey) => normalize(recordKey) === normalizedKey,
  );
}

function getResponseError(response: WebSocketMessage, fallback: string): string {
  return response.messageType === "ERROR" && typeof response.error === "string"
    ? response.error
    : fallback;
}

export default function ScoreBoard({
  gameView,
  onSwitchToWaitingRoom,
  onSwitchToMenu,
}: ScoreBoardProps) {
  const { endGameAWFR, leaveRoomAWFR, latestMessage } = useGameSocketContext();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [actionError, setActionError] = useState("");
  const navigationTargetRef = useRef<NavigationTarget>(null);

  // ENDGAME_RESPONSE is broadcast to everyone in the room. A player who did
  // not press a button is therefore moved from the scoreboard to the room too.
  useEffect(() => {
    const currentGameId = localStorage.getItem("gameId");

    if (
      latestMessage?.messageType === "ENDGAME_RESPONSE" &&
      navigationTargetRef.current === null &&
      currentGameId !== null &&
      latestMessage.gameId === currentGameId) {
        onSwitchToWaitingRoom();
        localStorage.removeItem("gameId");
    }
  }, [latestMessage, onSwitchToWaitingRoom]);

  const result = useMemo(() => {
    const { state, scores, winner } = gameView;
    const winnerKey = winner == null ? "" : normalize(winner);

    const factions: FactionResult[] = state.factions.map((faction) => {
      const scoreKey = findMatchingKey(scores, faction);

      return {
        name: faction,
        hp: scoreKey ? scores[scoreKey] : 0,
        isWinner: normalize(faction) === winnerKey,
      };
    });

    const winningFaction = factions.find((faction) => faction.isWinner);
    const highestHp = Math.max(...factions.map((faction) => faction.hp));
    const highestHpFactions = factions.filter(
      (faction) => faction.hp === highestHp,
    );
    const inferredWinner =
      !winner && highestHpFactions.length === 1 ? highestHpFactions[0] : null;

    if (inferredWinner) {
      inferredWinner.isWinner = true;
    }

    const isDraw = ["draw", "tie", "remis"].includes(winnerKey);

    return {
      factions,
      winnerLabel: isDraw
        ? "Draw"
        : toLabel(
            winner || winningFaction?.name || inferredWinner?.name || "Unknown",
          ),
      winnerFaction: winningFaction?.name ?? inferredWinner?.name ?? "",
      isDraw,
      roomName: localStorage.getItem("room") ?? "Current room",
    };
  }, [gameView]);

  async function endCurrentGame(): Promise<boolean> {
    const response = await endGameAWFR();

    if (response.messageType !== "ENDGAME_RESPONSE") {
      setActionError(getResponseError(response, "Could not end the game."));
      return false;
    }

    localStorage.removeItem("gameId");
    return true;
  }

  async function handleReturnToRoom() {
    if (isSubmitting) {
      return;
    }

    navigationTargetRef.current = "room";
    setIsSubmitting(true);
    setActionError("");

    try {
      if (await endCurrentGame()) {
        onSwitchToWaitingRoom();
        return;
      }
    } catch (error) {
      setActionError(
        error instanceof Error ? error.message : "Could not end the game.",
      );
    } finally {
      navigationTargetRef.current = null;
      setIsSubmitting(false);
    }
  }

  async function handleReturnToMenu() {
    if (isSubmitting) {
      return;
    }

    navigationTargetRef.current = "menu";
    setIsSubmitting(true);
    setActionError("");

    try {
      if (!(await endCurrentGame())) {
        return;
      }

      const leaveResponse = await leaveRoomAWFR();
      if (leaveResponse.messageType !== "LEAVEROOM_RESPONSE") {
        setActionError(
          getResponseError(leaveResponse, "The game ended, but the room could not be left."),
        );
        return;
      }

      localStorage.removeItem("room");
      localStorage.removeItem("gameId");
      onSwitchToMenu();
    } catch (error) {
      setActionError(
        error instanceof Error
          ? error.message
          : "Could not return to the menu.",
      );
    } finally {
      navigationTargetRef.current = null;
      setIsSubmitting(false);
    }
  }

  const [leftFaction, rightFaction] = result.factions;
  const winnerImage = result.winnerFaction
    ? imagesByName[`${normalize(result.winnerFaction)}/sztab`]
    : undefined;

  return (
    <main className="score-screen">
      <div className="score-screen__noise" aria-hidden="true" />

      <div className="score-screen__shell">
        <header className="score-screen__header">
          <div>
            <p className="score-screen__eyebrow">After-action report</p>
            <h1>Battle complete</h1>
            <p className="score-screen__intro">
              Final result for <strong>{result.roomName}</strong>
            </p>
          </div>

          <div className="score-screen__header-actions">
            <Button
              className="score-button score-button--ghost"
              text={isSubmitting ? "Finishing…" : "Return to room"}
              onClick={() => void handleReturnToRoom()}
              disabled={isSubmitting}
            />
            <Button
              className="score-button score-button--danger"
              text={isSubmitting ? "Finishing…" : "Return to menu"}
              onClick={() => void handleReturnToMenu()}
              disabled={isSubmitting}
            />
          </div>
        </header>

        <section className="winner-panel war-result-panel" aria-label="Winner">
          <div className="winner-panel__emblem" aria-hidden="true">
            {winnerImage ? <img src={winnerImage} alt="" /> : <span>◆</span>}
          </div>

          <div className="winner-panel__content">
            <span>{result.isDraw ? "Final result" : "Winner"}</span>
            <strong>{result.winnerLabel}</strong>
            {!result.isDraw && result.winnerFaction && (
              <small>{toLabel(result.winnerFaction)} faction</small>
            )}
          </div>

          <div className="winner-panel__stamp" aria-hidden="true">
            {result.isDraw ? "DRAW" : "VICTOR"}
          </div>
        </section>

        <section className="score-panel war-result-panel" aria-label="Final score">
          <div className="score-section-heading">
            <div>
              <p className="score-section-heading__number">01 / Final result</p>
              <h2>Final score</h2>
            </div>
            <p>Headquarters HP remaining when the match ended.</p>
          </div>

          <div className="scoreline">
            <span className="scoreline__faction">
              {toLabel(leftFaction.name)}
            </span>
            <strong className="scoreline__value">{leftFaction.hp}</strong>
            <span className="scoreline__separator">:</span>
            <strong className="scoreline__value">{rightFaction.hp}</strong>
            <span className="scoreline__faction scoreline__faction--right">
              {toLabel(rightFaction.name)}
            </span>
          </div>
        </section>

        <section className="faction-results" aria-label="Faction headquarters HP">
          {result.factions.map((faction, index) => {
            const factionName = normalize(faction.name);
            const factionImage = imagesByName[`${factionName}/sztab`];

            return (
              <article
                className={`faction-result faction-result--${factionName}${
                  faction.isWinner ? " is-winner" : ""
                }`}
                key={faction.name}
              >
                <div className="faction-result__index">0{index + 1}</div>

                <div className="faction-result__emblem" aria-hidden="true">
                  {factionImage ? (
                    <img src={factionImage} alt="" />
                  ) : (
                    <span>{index + 1}</span>
                  )}
                </div>

                <div className="faction-result__identity">
                  <span>{faction.isWinner ? "Winning faction" : "Faction"}</span>
                  <h2>{toLabel(faction.name)}</h2>
                </div>

                <div className="faction-result__hp">
                  <span>Headquarters HP</span>
                  <strong>{faction.hp}</strong>
                </div>
              </article>
            );
          })}
        </section>

        {actionError && (
          <p className="score-error" role="alert">
            {actionError}
          </p>
        )}
      </div>
    </main>
  );
}
