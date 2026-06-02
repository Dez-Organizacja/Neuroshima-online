import React from "react";
import "./GameButton.css";
import { ActionData } from "./ActionTypes";
import { useGameSocketContext } from "../websockets/gameSocketContext";
import { GameState } from "../Dlaigora";

interface GameButtonProps {
    x: number;
    y: number;
    width: number;
    height: number;
    text: string;
    sendAction? : (action : ActionData) => void;
    children?: React.ReactNode;
    onClick?: () => void;
    gameState: GameState;
}

export function ClickButton(text: string, sendAction : ((action : ActionData) => void) | undefined, gameState: GameState | undefined): void {
    // const {sendAction} = useGameSocketContext();
    if(!gameState) return;
    const field = gameState.view.availableActions.buttons.find(field => field === text);
    if(!field) return;
    if(!sendAction){
        return;
    }
    if(text === "End Turn") {
        console.log("Your turn has ended.")
        const action: ActionData = {
            type: "button",
            name: "end_turn"
        }
        sendAction(action);
    } else if(text === "Cancel") {
        console.log("Cancel.");

        const action: ActionData = {
            type: "button",
            name: "cancel"
        }
        sendAction(action);
    } else if(text === "Discard") {
        console.log("Discard.");
        const action: ActionData = {
            type: "button",
            name: "discard"
        }
        sendAction(action);
    }
}

export default function GameButton({
    x,
    y,
    width,
    height,
    text,
    sendAction,
    children,
    onClick,
    gameState
}: GameButtonProps) {

    return (
        <div
            className="game-button"

            // onClick={onClick}
            onClick={() => ClickButton(text, sendAction, gameState)}

            style={{
                left: x,
                top: y,
                width: width,
                height: height
            }}
        >
            {text}
            {children}
        </div>
    );
}