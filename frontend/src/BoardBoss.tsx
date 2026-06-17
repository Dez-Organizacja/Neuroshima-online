import React, { useState, useEffect, useRef, useMemo } from "react";
import { useGameSocketContext } from "./websockets/gameSocketContext"; 
import { useProcesedGameState, GameState } from "./Dlaigora";
import HexTest from "./HexTest";

export default function Display() {
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

        console.log("GAMESTATE RECEIVED - HURAAAAA!");
        console.log(gameState);

        let ActiveGameState: GameState = structuredClone(gameState);
        let LastGameState: GameState = structuredClone(gameState);
        if(prevGameState) ActiveGameState = structuredClone(prevGameState);

        // === Czyszczenie prev animacji === //
        ActiveGameState.view.animations.length = 0;


        console.log("----- WHILE -----");

        let i: number = 0;
        while(LastGameState.view.animations.length > i) {

            // ================= //
            console.log(ActiveGameState);
            // ================= //

            const CurrentAnimation = LastGameState.view.animations[i];

            if(CurrentAnimation.type === "attack") {
                screens.push(
                    <HexTest gameState={ActiveGameState} attackingUnit={CurrentAnimation.attacker} targetUnit={CurrentAnimation.target} />
                )

            } else if(CurrentAnimation.type === "destroy") {
                const IndexToRemove = ActiveGameState.view.state.board.findIndex(item =>
                    item.pos === LastGameState.view.animations[i].target
                );
                if(IndexToRemove !== -1) {
                    console.log("DESTROY " + CurrentAnimation);
                    ActiveGameState.view.state.board.splice(IndexToRemove, 1);
                }

                screens.push(
                    <HexTest gameState={ActiveGameState} />
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

                screens.push(
                    <HexTest gameState={ActiveGameState} />
                )

            } else if(CurrentAnimation.type === "weaken") {
                const CurrentIndex = ActiveGameState.view.state.board.findIndex(item =>
                    item.pos === CurrentAnimation.target
                );
                if(CurrentIndex !== -1) {
                    console.log("WEAKEN " + CurrentAnimation);
                    ActiveGameState.view.state.board[CurrentIndex].unit.wounds = 0;
                    ActiveGameState.view.state.board[CurrentIndex].unit.damage += CurrentAnimation.damage;
                }

                screens.push(
                    <HexTest gameState={ActiveGameState} />
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

    const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

    useEffect(() => {
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

    if (!gameState || AllScreens.length === 0) {
        return null;
    }

    return <>{AllScreens[currentIndex]}</>;



    // ===== Wersja bez animacji ===== //
    // return (
    //     <HexTest gameState={gameState} />
    // )
}