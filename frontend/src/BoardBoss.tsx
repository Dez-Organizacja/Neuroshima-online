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

        const screens = [];

        const States: GameState[] = [];

        console.log("GAMESTATE RECEIVED - HURAAAAA!");
        console.log(gameState);
        console.log(prevGameState)

        let ActiveGameState: GameState = structuredClone(gameState);
        let LastGameState: GameState = structuredClone(gameState);
        if(prevGameState) ActiveGameState = structuredClone(prevGameState);

        // === Czyszczenie prev animacji === //
        ActiveGameState.view.animations.length = 0;
        ActiveGameState.view.availableActions.board.length = 0;
        ActiveGameState.view.availableActions.hand.length = 0;
        ActiveGameState.view.state.hands[ActiveGameState.view.uiState.faction] = LastGameState.view.state.hands[ActiveGameState.view.uiState.faction];


        console.log("----- WHILE -----");

        let i: number = 0;
        while(LastGameState.view.animations.length > i) {

            // ================= //
            console.log(ActiveGameState);
            // ================= //

            const CurrentAnimation = LastGameState.view.animations[i];

            if(CurrentAnimation.type === "attack") {
                console.log("ATTACK " + CurrentAnimation.target[0] + ", " + CurrentAnimation.target[1] + "    i: " + i)
                States.push(
                    structuredClone(ActiveGameState)
                );
                screens.push(
                    <HexTest gameState={States[i]} attackingUnit={CurrentAnimation.attacker} targetUnit={CurrentAnimation.target} isAnimation={true} />
                )

            } else if(CurrentAnimation.type === "destroy") {
                const IndexToRemove = ActiveGameState.view.state.board.findIndex(item =>
                    item.pos[0] === CurrentAnimation.target[0] &&
                    item.pos[1] === CurrentAnimation.target[1]
                );
                if(IndexToRemove !== -1) {
                    console.log("DESTROY " + CurrentAnimation.target[0] + ", " + CurrentAnimation.target[1] + "    i: " + i);
                    ActiveGameState.view.state.board.splice(IndexToRemove, 1);
                }

                States.push(
                    structuredClone(ActiveGameState)
                );
                screens.push(
                    <HexTest gameState={States[i]} isAnimation={true} />
                )

            } else if(CurrentAnimation.type === "wound") {
                const CIndex = ActiveGameState.view.state.board.findIndex(item =>
                    item.pos[0] === CurrentAnimation.target[0] &&
                    item.pos[1] === CurrentAnimation.target[1]
                );
                if(CIndex !== -1) {
                    console.log("WOUND " + CurrentAnimation.target[0] + ", " + CurrentAnimation.target[1] + "    i: " + i);
                    ActiveGameState.view.state.board[CIndex].unit.wounds += CurrentAnimation.wounds;
                    console.log("WOUNDS IN TOTAL: " + ActiveGameState.view.state.board[CIndex].unit.wounds);
                }

                States.push(
                    structuredClone(ActiveGameState)
                );
                screens.push(
                    <HexTest gameState={States[i]} isAnimation={true} />
                )

            } else if(CurrentAnimation.type === "weaken") {
                const CurrentIndex = ActiveGameState.view.state.board.findIndex(item =>
                    item.pos[0] === CurrentAnimation.target[0] &&
                    item.pos[1] === CurrentAnimation.target[1]
                );
                if(CurrentIndex !== -1) {
                    console.log("WEAKEN " + CurrentAnimation.target[0] + ", " + CurrentAnimation.target[1] + "    i: " + i);
                    ActiveGameState.view.state.board[CurrentIndex].unit.wounds = 0;
                    ActiveGameState.view.state.board[CurrentIndex].unit.damage += CurrentAnimation.damage;
                }

                States.push(
                    structuredClone(ActiveGameState)
                );
                screens.push(
                    <HexTest gameState={States[i]} isAnimation={true} />
                )

            } else if(CurrentAnimation.type === "set_wire") {

                
                const CurrentIndex = ActiveGameState.view.state.board.findIndex(item =>
                    item.pos[0] === CurrentAnimation.target[0] &&
                    item.pos[1] === CurrentAnimation.target[1]
                );
                if(CurrentIndex !== -1) {
                    console.log("SET_WIRE " + CurrentAnimation.target[0] + ", " + CurrentAnimation.target[1] + "    i: " + i);
                    ActiveGameState.view.state.board[CurrentIndex].unit.wired = CurrentAnimation.wired;
                }

                States.push(
                    structuredClone(ActiveGameState)
                );
                screens.push(
                    <HexTest gameState={States[i]} isAnimation={true} />
                )
            }

            i += 1;
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