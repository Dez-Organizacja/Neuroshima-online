import React, { useState, useEffect, useRef, useMemo } from "react";
import { useGameSocketContext } from "./websockets/gameSocketContext"; 
import { useProcesedGameState, GameState } from "./Dlaigora";
import HexTest from "./HexTest";
import ScoreBoard from "./Score";

const ANIMATION_FRAME_MS = 750;
const SCOREBOARD_DELAY_MS = 2_000;

type BoardBossProps = {
  onSwitchToMenu: () => void;
  onSwitchToWaitingRoom: () => void;
};

export default function Display({onSwitchToMenu, onSwitchToWaitingRoom} : BoardBossProps) {
    const { gameState, prevGameState} = useProcesedGameState();

    // const AllScreens = [];

    // ======================== //
    // if(currentIndex === 0) {
    // ======================== //


    const AllScreens = useMemo(() => {
        if(!gameState) {
            console.log("NO GAMESTATE RECEIVED");
            // return (<div>No Game State Received.</div>);
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
        if(LastGameState.view.animations[0] !== undefined) {
            const RAnimation = LastGameState.view.animations[0];
            if(LastGameState.view.animations[0].type === "rotation") {
                const RIndex = ActiveGameState.view.state.board.findIndex(field =>
                    field.pos[0] === RAnimation.target[0] &&
                    field.pos[1] === RAnimation.target[1]
                )
                if(RIndex !== -1) {
                    ActiveGameState.view.state.board[RIndex].unit.rotation = LastGameState.view.animations[0].rotation;
                    LastGameState.view.animations.splice(0, 1);
                }
            }
        }

        if(LastGameState.view.animations[0] !== undefined) {
            const RAnimation = LastGameState.view.animations[0];
            if(LastGameState.view.animations[0].type === "rotation") {
                const RIndex = ActiveGameState.view.state.board.findIndex(field =>
                    field.pos[0] === RAnimation.target[0] &&
                    field.pos[1] === RAnimation.target[1]
                )
                if(RIndex !== -1) {
                    ActiveGameState.view.state.board[RIndex].unit.rotation = LastGameState.view.animations[0].rotation;
                    LastGameState.view.animations.splice(0, 1);
                }
            }
        }

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


        console.log("Last: ");
        console.log(LastGameState);

        screens.push(
            <HexTest gameState={LastGameState} />
        )

        console.log("Last tried to display.");

        return screens;

    }, [gameState]);

    // }


    // Wyswietlanie z odstepami

    const [currentIndex, setCurrentIndex] = useState(0);
    const [showScoreboard, setShowScoreboard] = useState(false);
    const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

    useEffect(() => {
        setShowScoreboard(false);
        if (AllScreens.length === 0) return;

        setCurrentIndex(0);

        if (intervalRef.current !== null) {
            clearInterval(intervalRef.current);
        }

        intervalRef.current = setInterval(() => {
            setCurrentIndex(prev => {
                if (prev >= AllScreens.length - 1) {
                    if (intervalRef.current !== null) {
                        clearInterval(intervalRef.current);
                        intervalRef.current = null;
                    }
                    return prev;
                }
                return prev + 1;
            });
        }, 750);

        return () => {
            if (intervalRef.current !== null) {
                clearInterval(intervalRef.current);
                intervalRef.current = null;
            }
        };
    }, [gameState]);

    useEffect(() => {
        if (!gameState || gameState.view.phase !== "gameover") {
            return;
        }

        if (AllScreens.length === 0) {
            return;
        }

        const animationFinished =
            currentIndex >= AllScreens.length - 1;

        if (!animationFinished) {
            return;
        }

        const timeoutId = window.setTimeout(() => {
            setShowScoreboard(true);
        }, SCOREBOARD_DELAY_MS);

        return () => {
            window.clearTimeout(timeoutId);
        };
    }, [gameState, currentIndex, AllScreens.length]);

    if (showScoreboard && gameState.view.phase === "gameover") {
        return (
        <ScoreBoard
            onSwitchToMenu={onSwitchToMenu}
            onSwitchToWaitingRoom={onSwitchToWaitingRoom}
            gameView={gameState.view}
        />
        );
    }
    if (!gameState || AllScreens.length === 0) {
        return null;
    }

    return <>{AllScreens[currentIndex]}</>;



    // ===== Wersja bez animacji ===== //
    // return (
    //     <HexTest gameState={gameState} />
    // )
}