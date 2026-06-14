import React from "react";
import { useState, useContext, useEffect } from "react";
import { useGameSocketContext } from "../websockets/gameSocketContext";
import { useProcesedGameState, GameState } from "../Dlaigora";
import Hexagon from "./Hexagon";
import Image from "./HexImage";
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


    if(imageName !== "undefined/undefined") {

        // console.log("POZ: " + poz1 + ", " + poz2 + "    ROT: " + Rotation);

        // const Field = gameState.view.state.board.find(Field =>
        //     Field.pos[0] === poz1 &&
        //     Field.pos[1] === poz2
        // );
        // let PathSztab: string = "";
        // if(Field) PathSztab = Field.unit.faction + "/" + "sztab";
        // if(imageName === PathSztab) {
        //     const field = gameState.view.state.board.find(field =>
        //         field.pos[0] === poz1 &&
        //         field.pos[1] === poz2
        //     );
        //     if(field) {
        //         const HP = 20 - field.unit.damage;
        //         return (
        //             <div>
        //                 <Image imageName={imageName} x={x} y={y} poz1={poz1} poz2={poz2} height={height} rotation={Rotation} gameState={gameState} />
        //                 <Hexagon x={x} y={y} poz1={poz1} poz2={poz2} size={size} color={color} opacity={opacity} rotation={Rotation} sendAction={sendAction} gameState={gameState} > {HP} </Hexagon>
        //             </div>
        //         )
        //     }
        // } else {
            return (
                <div>
                    <Image imageName={imageName} x={x} y={y} poz1={poz1} poz2={poz2} height={height} rotation={Rotation} gameState={gameState} />
                    <Hexagon x={x} y={y} poz1={poz1} poz2={poz2} size={size} color={color} opacity={opacity} rotation={Rotation} sendAction={sendAction} gameState={gameState} />
                </div>
            )
        // }
    } else {
        return (
            <div>
                <Hexagon x={x} y={y} poz1={poz1} poz2={poz2} size={size} color={color} opacity={opacity} rotation={Rotation} sendAction={sendAction} gameState={gameState} />
            </div>
        )
    }
}

export default Tile;