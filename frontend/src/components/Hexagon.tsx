import React from "react";
import { useState, useContext } from "react";
import "./Hexagon.css";
import { ActionData } from "./ActionTypes"
import { useGameSocketContext } from "../websockets/gameSocketContext";
import { useProcesedGameState, GameState } from "../Dlaigora";

type HexagonProps = {
    x: number;
    y: number;
    poz1: number;
    poz2: number;
    size?: number;
    color?: string;
    opacity?: number;
    rotation?: number;
    onClick?: () => void;
    children?: React.ReactNode;
    sendAction? : (action : ActionData) => void;
    gameState? : GameState;
};

export function ClickCheck(x: number, y: number, gameState : GameState | undefined, sendAction : ((action : ActionData) => void) | undefined) : void {
    if(y === 999) return;
    if(!gameState){
        return;
    }
    if(!sendAction){
        return;
    }
    if(y === -1) {
        if(gameState.view.availableActions.hand[x]) {
            console.log("Click accepted (hand) : ", { x, y });
            const action: ActionData = {
                type: "hand",
                slot: x
            };
            sendAction(action);
        }
    } else {
        const Pair = [x, y];
        const field = gameState.view.availableActions.board.find(field =>
            field[0] === Pair[0] &&
            field[1] === Pair[1]
        );
        if(field) {
            console.log("Click accepted (board) : ", { x, y });

            const Pair = [x, y];
            const action: ActionData = {
                type: "board",
                pos: Pair
            };
            sendAction(action);
        }
    }
}

const Hexagon: React.FC<HexagonProps> = ({
    x,
    y,
    poz1,
    poz2,
    size = 100,
    color = "#4CAF50",
    opacity = 0.3,
    rotation = 0,
    onClick,
    children,
    sendAction,
    gameState,
}) => {
    const height = size * 0.866;

    return (
        <div
            className="hexagon"
            // onClick={onClick}
            // onClick={() => console.log("Clicked hex:", { poz1, poz2 })}
            onClick={() => ClickCheck(poz1, poz2, gameState, sendAction)}
        style={{
            width: size,
            height: height,
            backgroundColor: color,
            opacity: opacity,
            position: "absolute",
            left: x - (size / 2),
            top: y - (height / 2),
            transform: `rotate(${rotation}deg) scale(1)`,
        }}
        >
        < div className="hexagon-content">{children}</div>
         </div>
    );
};

export default Hexagon;