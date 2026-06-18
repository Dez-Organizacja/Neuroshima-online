import React from "react";
import "./RotateButton.css"

interface RotateButtonProps {
    x: number;
    y: number;
    width: number;
    height: number;
    text: string;
    onClick?: () => void;
    clickable?: boolean;
    type: string;
}

function ClickButton(text: string, type: string, clickable: boolean)
{
    if(!clickable) return;

    if(type === "left") {
        // const sendLeftArrow = () => {
            window.dispatchEvent(
                new KeyboardEvent("keydown", {
                    key: "ArrowLeft",
                })
            );
        // };
    } else if(type === "right") {
        // const sendRightArrow = () => {
            window.dispatchEvent(
                new KeyboardEvent("keydown", {
                    key: "ArrowRight",
                })
            );
        // };
    }
}

export default function RotateButton({
    x,
    y,
    width,
    height,
    text,
    onClick,
    clickable = true,
    type,
}: RotateButtonProps) {
    return (
            <div
                className="game-button rotate-button"
    
                // onClick={onClick}
                onClick={() => ClickButton(text, type, clickable)}
    
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