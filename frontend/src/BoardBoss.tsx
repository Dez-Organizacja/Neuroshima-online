import { useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import { useProcesedGameState, type GameState } from "./Dlaigora";
import HexTest from "./HexTest";
import ScoreBoard from "./Score";

const ANIMATION_FRAME_MS = 750;
const SCOREBOARD_DELAY_MS = 2_000;

type BoardBossProps = {
  onSwitchToMenu: () => void;
  onSwitchToWaitingRoom: () => void;
};

export default function Display({
  onSwitchToMenu,
  onSwitchToWaitingRoom,
}: BoardBossProps) {
  const { gameState, prevGameState } = useProcesedGameState();
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showScoreboard, setShowScoreboard] = useState(false);

  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const allScreens = useMemo(() => {
    if (!gameState) {
      return [];
    }

    const screens: ReactNode[] = [];
    const activeGameState: GameState = structuredClone(
      prevGameState ?? gameState,
    );
    const lastGameState: GameState = structuredClone(gameState);

    activeGameState.view.animations = [];

    const animations = Array.isArray(lastGameState.view.animations)
      ? lastGameState.view.animations
      : [];

    animations.forEach((currentAnimation, animationIndex) => {
      if (currentAnimation.type === "attack") {
        screens.push(
          <HexTest
            key={`attack-${animationIndex}`}
            gameState={structuredClone(activeGameState)}
            attackingUnit={currentAnimation.attacker}
            targetUnit={currentAnimation.target}
          />,
        );
        return;
      }

      if (currentAnimation.type === "destroy") {
        const indexToRemove = activeGameState.view.state.board.findIndex(
          (item) =>
            item.pos[0] === currentAnimation.target[0] &&
            item.pos[1] === currentAnimation.target[1],
        );

        if (indexToRemove !== -1) {
          activeGameState.view.state.board.splice(indexToRemove, 1);
        }
      }

      if (currentAnimation.type === "wound") {
        const boardIndex = activeGameState.view.state.board.findIndex(
          (item) =>
            item.pos[0] === currentAnimation.target[0] &&
            item.pos[1] === currentAnimation.target[1],
        );

        if (boardIndex !== -1) {
          activeGameState.view.state.board[boardIndex].unit.wounds +=
            currentAnimation.wounds;
        }
      }

      if (currentAnimation.type === "weaken") {
        const boardIndex = activeGameState.view.state.board.findIndex(
          (item) =>
            item.pos[0] === currentAnimation.target[0] &&
            item.pos[1] === currentAnimation.target[1],
        );

        if (boardIndex !== -1) {
          activeGameState.view.state.board[boardIndex].unit.wounds = 0;
          activeGameState.view.state.board[boardIndex].unit.damage +=
            currentAnimation.damage;
        }
      }

      screens.push(
        <HexTest
          key={`${currentAnimation.type}-${animationIndex}`}
          gameState={structuredClone(activeGameState)}
        />,
      );
    });

    screens.push(
      <HexTest key="final-board" gameState={lastGameState} />,
    );

    return screens;
  }, [gameState, prevGameState]);

  useEffect(() => {
    setCurrentIndex(0);
    setShowScoreboard(false);

    if (intervalRef.current !== null) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }

    if (allScreens.length <= 1) {
      return;
    }

    intervalRef.current = setInterval(() => {
      setCurrentIndex((previousIndex) => {
        if (previousIndex >= allScreens.length - 1) {
          if (intervalRef.current !== null) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
          }
          return previousIndex;
        }

        return previousIndex + 1;
      });
    }, ANIMATION_FRAME_MS);

    return () => {
      if (intervalRef.current !== null) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [allScreens]);
  useEffect(() => {
    if (
      gameState?.view.phase !== "gameover" ||
      allScreens.length === 0 ||
      currentIndex < allScreens.length - 1
    ) {
      return;
    }

    const timeoutId = window.setTimeout(() => {
      setShowScoreboard(true);
    }, SCOREBOARD_DELAY_MS);

    return () => {
      window.clearTimeout(timeoutId);
    };
  }, [allScreens.length, currentIndex, gameState?.view.phase]);

  if (!gameState || allScreens.length === 0) {
    return (
      <main style={{ color: "white", padding: "2rem" }}>
        Loading game state…
      </main>
    );
  }

  if (showScoreboard && gameState.view.phase === "gameover") {
    return (
      <ScoreBoard
        onSwitchToMenu={onSwitchToMenu}
        onSwitchToWaitingRoom={onSwitchToWaitingRoom}
        gameView={gameState.view}
      />
    );
  }

  const safeCurrentIndex = Math.min(currentIndex, allScreens.length - 1);
  return <>{allScreens[safeCurrentIndex]}</>;
}