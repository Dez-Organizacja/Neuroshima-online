import React from "react";
import { useState, useContext, useEffect } from "react";
import { useGameSocketContext } from "../websockets/gameSocketContext";
import { useProcesedGameState, GameState } from "../Dlaigora";
import Hexagon from "./Hexagon";
import Image from "./HexImage";
import NumberOverlay from "./NumberOverlay";
import { ActionData } from "./ActionTypes";

type TileProps = {
    imageName: string;
    x: number;
    y: number;
    poz1: number;
    poz2: number;
    size?: number;
    color?: string;
    opacity?: number;
    rotation: number;
    sendAction?: (action: ActionData) => void;
    gameState: GameState;
};

const Tile: React.FC<TileProps> = ({
    imageName,
    x,
    y,
    poz1,
    poz2,
    size = 100,
    color = "#4CAF50",
    opacity = 0.3,
    rotation,
    sendAction,
    gameState,
}) => {

    const Items = [];

    // console.log("START1 = POZ: " + poz1 + ", " + poz2 + "    ROT: " + rotation);


    const height = size * 0.866;

    const canRotate = gameState.view.uiState.mode === "rotation";
    const [Rotation, setRotation] = useState(rotation);

    // console.log("START2 = POZ: " + poz1 + ", " + poz2 + "    ROT: " + Rotation);


    useEffect(() => {
        setRotation(rotation);
    }, [rotation]);

    useEffect(() => {

        const handleKeyDown = (event: KeyboardEvent) => {
            if(!canRotate) return;
            const field = gameState.view.availableActions.board.find(field =>
                field[0] === poz1 &&
                field[1] === poz2
            );
            if(!field) return;
            // console.log("hjgjh");

            if (event.key === "ArrowLeft") {
                setRotation(prev => (prev + 300) % 360);
            }

            if (event.key === "ArrowRight") {
                setRotation(prev => (prev + 60) % 360);
            }
        };

        window.addEventListener("keydown", handleKeyDown);

        return () => {
            window.removeEventListener("keydown", handleKeyDown);
        };

    }, [canRotate]);

    if(color === "#666666") opacity = 0.5;
    if(imageName === "undefined/undefined") opacity = 0.5;


    console.log("LAST CLICK (" + poz1 + ", " + poz2 + "):");
    console.log(gameState.view.LastClickedHex);
    if(gameState.view.LastClickedHex !== undefined) {
        console.log("LAST CLICK (CLICKED):");
        console.log(gameState.view.LastClickedHex);
        if(gameState.view.LastClickedHex.source === "board" && gameState.view.LastClickedHex.pos[0] === poz1 && gameState.view.LastClickedHex.pos[1] === poz2) {
            Items.push(
                <Hexagon x={x} y={y} poz1={poz1} poz2={poz2} size={size + 10} color={"#b0ff97"} opacity={0.7} rotation={Rotation} sendAction={sendAction} gameState={gameState} />
            )
        }
        if(gameState.view.LastClickedHex.source === "hand" && gameState.view.LastClickedHex.slot === poz1 && poz2 === -1) {
            Items.push(
                <Hexagon x={x} y={y} poz1={poz1} poz2={poz2} size={size + 10} color={"#b0ff97"} opacity={0.7} rotation={Rotation} sendAction={sendAction} gameState={gameState} />
            )
        }
    }


    if(imageName !== "undefined/undefined") {

        Items.push(
            <Image imageName={imageName} x={x} y={y} poz1={poz1} poz2={poz2} height={height} rotation={Rotation} gameState={gameState} />
        )

        // ===== Wired and Wounds ===== //
        const Field = gameState.view.state.board.find(Field =>
            Field.pos[0] === poz1 &&
            Field.pos[1] === poz2
        );
        let Wired: boolean = false;
        if(Field) Wired = Field.unit.wired;
        if(Wired === true) {
            Items.push(
                <Image imageName="inne/siec2" x={x} y={y} poz1={poz1} poz2={poz2} height={size} rotation={0} gameState={gameState} opacity={0.6} />
            )
        }

        let Wounds: number = 0;
        if(Field) Wounds = Field.unit.wounds;

        if(Wounds !== 0) {
            Items.push(
                <Image imageName="inne/rana2" x={x} y={y} poz1={poz1} poz2={poz2} height={size / 3} rotation={0} gameState={gameState} />
            )
            Items.push(
                <NumberOverlay x={x} y={y} value={Wounds} opacity={0.9} height={size / 6} />
            )
        }
        // ===== ================ ===== //

        Items.push(
            <Hexagon x={x} y={y} poz1={poz1} poz2={poz2} size={size} color={color} opacity={opacity} rotation={Rotation} sendAction={sendAction} gameState={gameState} />
        )

        // console.log("POZ: " + poz1 + ", " + poz2 + "    ROT: " + Rotation);

        return (
            <div>
                {Items}
            </div>
        )
    } else {
        Items.push(
            <Hexagon x={x} y={y} poz1={poz1} poz2={poz2} size={size} color={color} opacity={opacity} rotation={Rotation} sendAction={sendAction} gameState={gameState} />
        )
        return(
            <div>
                {Items}
            </div>
        )
    }
}

export default Tile;