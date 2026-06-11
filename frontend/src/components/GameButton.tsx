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
    // if(gameState.view.uiState.mode === "rotation") return;

    console.log("ACTION: " + text);
    const action: ActionData = {
        type: "button",
        name: text
    }
    sendAction(action);
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

    let DisplayText: string = "";
    if(text === "end_turn") {DisplayText="End Turn";}
    if(text === "cancel") {DisplayText="Cancel";}
    if(text === "discard") {DisplayText="Discard";}
    if(text === "use") {DisplayText="Use";}
    if(text === "yes") {DisplayText="Yes";}
    if(text === "no") {DisplayText="No";}

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
            {DisplayText}
            {children}
        </div>
    );
}