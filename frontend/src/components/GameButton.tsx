import React from "react";
import "./GameButton.css";
import { ActionData } from "./ActionTypes";

interface GameButtonProps {
    x: number;
    y: number;
    width: number;
    height: number;
    text: string;
    onClick?: () => void;
}

export function ClickButton(text: string): void {
    if(text === "End Turn") {
        console.log("Your turn has ended.")

        const action: ActionData = {
            type: "button",
            name: "end_turn"
        }
    } else if(text === "Cancel") {
        console.log("Cancel.");

        const action: ActionData = {
            type: "button",
            name: "cancel"
        }
    } else if(text === "Discard") {
        console.log("Discard.");

        const action: ActionData = {
            type: "button",
            name: "discard"
        }
    }
}

export default function GameButton({
    x,
    y,
    width,
    height,
    text,
    onClick
}: GameButtonProps) {

    return (
        <div
            className="game-button"

            // onClick={onClick}
            onClick={() => ClickButton(text)}

            style={{
                left: x,
                top: y,
                width: width,
                height: height
            }}
        >
            {text}
        </div>
    );
}