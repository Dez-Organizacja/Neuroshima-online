import React from "react";
import { useState, useContext, useEffect } from "react";
import { GameState } from "../Dlaigora";
import "./TextBox.css"

type TextBoxProps = {
    text: string;
    x: number;
    y: number;
};

const TextBox: React.FC<TextBoxProps> = ({
    text,
    x,
    y,
}) => {
    return (
        <div
            className="text-box"
            style={{
                left: x,
                top: y,
            }}
        >
            {text}
        </div>
    )
}

export default TextBox;