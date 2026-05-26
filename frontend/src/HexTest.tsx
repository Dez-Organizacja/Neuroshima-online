import React, { useState } from "react";
import Hexagon from "./components/Hexagon";
import Image from "./components/HexImage";
import GetWindowSize from "./GetScreenSize";
import { imagesByName } from "./Images";
import { GameData } from "./components/GameData";

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

    // console.log("Width: " + ScreenWidth + "     Height: " + ScreenHeight);
    // console.log("CenterX: " + CenterX + "     CenterY: " + CenterY);
    // console.log("MidX: " + MidX + "     MidY: " + MidY);

    const Items = [];

    // =============== //

    
                // =================== Testowanie inputu =================== //
                console.log(GameData.view.uiState.message);

                console.log(GameData.view.state.board);

                console.log(GameData.view.state.hands.borgo.tokens);
                // =================== ================= =================== //



    // =================== Nowe Wyswietlanie =================== //

    for(let y = 0; y <= 4; y++){
        let xs = Math.abs(2 - y);
        let xf = 4 + Math.abs(2 - y) + 2 * Math.abs(2 - Math.abs(2 - y));
        console.log(y + " " + xs + "-" + xf);
        for(let x = Math.abs(2 - y); x <= 4 + Math.abs(2 - y) + 2 * Math.abs(2 - Math.abs(2 - y)); x+=2){
            const Y = y * 1.732 * Size;
            const X = x * Size;
            const FinalX = X + AddX;
            const FinalY = Y + AddY;

            // === Dict check === //
            const field = GameData.view.state.board.find(field =>
                field.pos[0] === y &&
                field.pos[1] === x
            );

            if (field) {
                const Path = field.unit.fraction + "/" + field.unit.name;
                console.log("{" + y + ", " + x +  "}  " + Path);

                Items.push(
                    <Image imageName={Path} x={FinalX} y={FinalY} height={((Size * 2 + 15) * 0.866)} rotation={30} />
                )
            }

            Items.push(
                <Hexagon x={FinalX} y={FinalY} poz1={y} poz2={x} size={Size * 2 + 15} rotation={30} color="#d10606"> {y}, {x} </Hexagon>
            )
        }
    }




    // Hand //
    const VerticalSpacing = 1.732 * Size;

    // keep whole hex visible
    const LeftX = Size + 10;
    const RightX = ScreenWidth - Size - 10;

    // vertically centered
    const StartY = CenterY - VerticalSpacing;

    const currentFraction = GameData.view.uiState.fraction;

    for (let i = -1; i <= 3; i+=2) {
        const FinalX = LeftX;
        const FinalY = StartY + i * VerticalSpacing;

        // === Dict check === //
        const Index = (i + 1) / 2;
        const TokenName = GameData.view.state.hands[currentFraction].tokens[Index];
        const Path = currentFraction + "/" + TokenName


        Items.push(
            <Image imageName={Path} x={FinalX} y={FinalY} height={((Size * 2 + 15) * 0.866)} rotation={30} />
        )

        Items.push(
            <Hexagon x={FinalX} y={FinalY} poz1={Index} poz2={-1} size={Size * 2 + 15} rotation={30} color="#00aaff" />
        )
    }
    // ======= Enemy Hand ======= //
    for( let i = -1; i <= 3; i+=2) {
        const FinalX = RightX;
        const FinalY = StartY + i * VerticalSpacing;
        // === Dict check === //
        const [enemyFraction, setEnemyFraction] = useState(GameData.view.state.fractions[0]);
        if(enemyFraction === currentFraction) setEnemyFraction(GameData.view.state.fractions[1]);
        const Index = (i + 1) / 2;
        const TokenName = GameData.view.state.hands[enemyFraction].tokens[Index];
        const Path = enemyFraction + "/" + TokenName
        Items.push(
            <Image imageName={Path} x={FinalX} y={FinalY} height={((Size * 2 + 15) * 0.866)} rotation={30} />
        )
        Items.push(
            <Hexagon x={FinalX} y={FinalY} poz1={Index} poz2={999} size={Size * 2 + 15} rotation={30} color="#00aaff" />
        )
    }
    // ======= ========== ======= //
    // ==== //

    // =================== ================= =================== //

    return (
        <div className="canvas">
            {Items}
        </div>
    )
}