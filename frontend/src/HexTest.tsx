import React from "react";
import Hexagon from "./components/Hexagon";
import Image from "./components/HexImage";
import GetWindowSize from "./GetScreenSize";
import { imagesByName } from "./Images";

async function cos(name : string) {
  console.log(name);
}

export default function HexTest(){
    const { width, height } = GetWindowSize();
    const ScreenWidth = width;
    const ScreenHeight = height;

    const Size = height / 12;

    const CenterX = ScreenWidth / 2;
    const CenterY = ScreenHeight / 2;
    const MidY = 2 * 1.732 * Size;
    const MidX = 4 * Size;
    const AddX = CenterX - MidX;
    const AddY = CenterY - MidY;

    console.log("Width: " + ScreenWidth + "     Height: " + ScreenHeight);
    console.log("CenterX: " + CenterX + "     CenterY: " + CenterY);
    console.log("MidX: " + MidX + "     MidY: " + MidY);

    const Items = [];

    // nowe koordynaty //
    for(let y = 0; y <= 4; y++){
        let xs = Math.abs(2 - y);
        let xf = 4 + Math.abs(2 - y) + 2 * Math.abs(2 - Math.abs(2 - y));
        console.log(y + " " + xs + "-" + xf);
        for(let x = Math.abs(2 - y); x <= 4 + Math.abs(2 - y) + 2 * Math.abs(2 - Math.abs(2 - y)); x+=2){
            const Y = y * 1.732 * Size;
            const X = x * Size;
            const FinalX = X + 300;
            const FinalY = Y + 300;

            Items.push(
                <Image imageName="silacz" x={FinalX} y={FinalY} height={((Size * 2 + 15) * 0.866)} rotation={30} />
            )
            Items.push(
                <Hexagon x={FinalX} y={FinalY} poz1={y} poz2={x} size={Size * 2 + 15} rotation={30} color="#d10606"> {y}, {x} </Hexagon>
            )
        }
    }

    Items.push(
        <Hexagon x={-95} y={-85} poz1={0} poz2={0} size={Size * 2 + 15} rotation={0} color="#d10606"> {0}, {0} </Hexagon>
    )

    // =============== //

    for(let q = -2; q <= 2; q++){
        const rMin = Math.max(-2, -q - 2);
        const rMax = Math.min(2, -q + 2);

        for(let r = rMin; r <= rMax; r++){

            const X = Size * (Math.sqrt(3) * q + Math.sqrt(3)/2 * r);
            const Y = Size * (3/2 * r);
            const FinalX = X + CenterX;
            const FinalY = Y + CenterY;
            // Items.push(
            // <Hexagon x={X} y={Y} poz1={q} poz2={r} size={Size * 2 - 5} rotation={30} color="#2196F3"> {q}, {r} </Hexagon>
            // )
            // Items.push(
            //     <Image imageName="silacz" x={X} y={Y} height={((Size * 2 - 5) * 0.866)} rotation={30} />
            // )
        }
    }

    return (
        <div className="canvas">
            {Items}
        </div>
    )
}