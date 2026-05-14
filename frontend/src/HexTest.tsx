import React from "react";
import Hexagon from "./components/Hexagon";
import GetWindowSize from "./GetScreenSize";

async function cos(name : string) {
  console.log(name);
}

export default function HexTest(){
    const { width, height } = GetWindowSize();
    const ScreenWidth = width;
    const ScreenHeight = height;

    const CenterX = ScreenWidth / 2;
    const CenterY = ScreenHeight / 2;

    const Size = height / 10;

    const Items = [];

    // nowe koordynaty //
    for(let y = 1; y <= 5; y++){
        let xs = 1 + Math.abs(3 - y);
        let xf = 5 + Math.abs(3 - y) + 2 * Math.abs(2 - Math.abs(3 - y));
        // console.log(y + " " + xs + "-" + xf);
        for(let x = 1 + Math.abs(3 - y); x <= 5 + Math.abs(3 - y) + 2 * Math.abs(2 - Math.abs(3 - y)); x+=2){
        }
    }
    // =============== //

    for(let q = -2; q <= 2; q++){
        const rMin = Math.max(-2, -q - 2);
        const rMax = Math.min(2, -q + 2);

        for(let r = rMin; r <= rMax; r++){

            const X = Size * (Math.sqrt(3) * q + Math.sqrt(3)/2 * r);
            const Y = Size * (3/2 * r);
            const FinalX = X + CenterX;
            const FinalY = Y + CenterY;
            Items.push(
            // <Hexagon x={X} y={Y} poz1={q} poz2={r} size={Size * 2 - 5} rotation={30} color="#2196F3" />
            <Hexagon x={X} y={Y} poz1={q} poz2={r} size={Size * 2 - 5} rotation={30} color="#2196F3"> {q}, {r} </Hexagon>
            )                                                                              
        }
    }

    return (
        <div>
            {Items}
        </div>
    )
}