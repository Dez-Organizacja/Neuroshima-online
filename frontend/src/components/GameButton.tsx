import React from "react";
import "./GameButton.css";

interface GameButtonProps {
    x: number;
    y: number;
    width: number;
    height: number;
    text: string;
    onClick?: () => void;
}

export function ClickButton(text: string): void {
    if(text === "End Turn") {console.log("Your turn has ended.")}
    else {console.log(text + ".")}
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