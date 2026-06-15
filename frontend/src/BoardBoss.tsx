import React, { useState } from "react";
import { useGameSocketContext } from "./websockets/gameSocketContext"; 
import { useProcesedGameState, GameState } from "./Dlaigora";
import HexTest from "./HexTest";

export default function Display() {
    const { gameState, prevGameState} = useProcesedGameState();
    if(gameState !== null) HexTest({gameState: gameState});
}