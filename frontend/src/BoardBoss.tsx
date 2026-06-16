import React, { useState, useEffect } from "react";
import { useGameSocketContext } from "./websockets/gameSocketContext"; 
import { useProcesedGameState, GameState } from "./Dlaigora";
import HexTest from "./HexTest";

export default function Display() {
    const { gameState, prevGameState} = useProcesedGameState();

    if(!gameState) return (<div>No Game State Received.</div>);
    let ActiveGameState: GameState = gameState;
    if(prevGameState) ActiveGameState = prevGameState;

    // === Czyszczenie prev animacji === //
    // ActiveGameState.view.animations.length = 0;

    // const AllScreens = [];

    // let i: number = 0;
    // while(gameState.view.animations.length > i) {
    //     const CurrentAnimation = gameState.view.animations[i];

    //     if(CurrentAnimation.type === "attack") {
    //         AllScreens.push(
    //             <HexTest gameState={ActiveGameState} attackingUnit={CurrentAnimation.attacker} targetUnit={CurrentAnimation.target} />
    //         )

    //     } else if(CurrentAnimation.type === "destroy") {
    //         const IndexToRemove = ActiveGameState.view.state.board.findIndex(item =>
    //             item.pos === gameState.view.animations[i].target
    //         );
    //         if(IndexToRemove !== -1) ActiveGameState.view.state.board.splice(IndexToRemove, 1);

    //         AllScreens.push(
    //             <HexTest gameState={ActiveGameState} />
    //         )

    //     } else if(CurrentAnimation.type === "wound") {
    //         const CurrentIndex = ActiveGameState.view.state.board.findIndex(item =>
    //             item.pos === CurrentAnimation.target
    //         );
    //         if(CurrentIndex !== -1) {
    //             ActiveGameState.view.state.board[CurrentIndex].unit.wounds += CurrentAnimation.wounds;
    //         }

    //         AllScreens.push(
    //             <HexTest gameState={ActiveGameState} />
    //         )

    //     } else if(CurrentAnimation.type === "weaken") {
    //         const CurrentIndex = ActiveGameState.view.state.board.findIndex(item =>
    //             item.pos === CurrentAnimation.target
    //         );
    //         if(CurrentIndex !== -1) {
    //             ActiveGameState.view.state.board[CurrentIndex].unit.wounds = 0;
    //             ActiveGameState.view.state.board[CurrentIndex].unit.damage += CurrentAnimation.damage;
    //         }

    //         AllScreens.push(
    //             <HexTest gameState={ActiveGameState} />
    //         )
    //     }

    //     i++;
    // }



    // // Wyswietlanie z odstepami
    // const [currentIndex, setCurrentIndex] = useState(0);

    // useEffect(() => {
    //     if (AllScreens.length === 0) return;

    //     const interval = setInterval(() => {
    //         setCurrentIndex(prev => {
    //             if (prev >= AllScreens.length - 1) {
    //                 clearInterval(interval);
    //                 return prev;
    //             }

    //             return prev + 1;
    //         });
    //     }, 250);

    //     return () => clearInterval(interval);
    // }, [AllScreens]);

    // return <>{AllScreens[currentIndex]}</>;



    // ===== Wersja bez animacji ===== //
    return (
        <HexTest gameState={gameState} />
    )
}