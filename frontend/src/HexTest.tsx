import { useState } from "react";
import Hexagon from "./components/Hexagon";
import Image from "./components/HexImage";
import GameButton from "./components/GameButton";
import GetWindowSize from "./GetScreenSize";
import { imagesByName } from "./Images";
import { useGameSocketContext } from "./websockets/gameSocketContext"; 
// import { gameState } from "./components/gameState";
// import { gameState } from "./components/gameState";
import { useProcesedGameState, GameState } from "./Dlaigora";
import Tile from "./components/Tile"
import TextBox from "./components/TextBox";
import { getCurrentFaction } from "./factionStore";

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
    const { sendAction } = useGameSocketContext();
    const { gameState} = useProcesedGameState();
    if (!gameState) {
        return <div>Loading game...</div>;
    }

    // const currentfaction = gameState.view.uiState.faction;
    const currentfaction = getCurrentFaction();
    if(!currentfaction){
        return <div>No faction found</div>;
    }
    const Items = [];
    // =============== //

    
                // =================== Testowanie inputu =================== //
                console.log(gameState.view.uiState.message);

                console.log(gameState.view.state.board);

                console.log(gameState.view.state.hands[currentfaction]?.tokens ?? []);
                // =================== ================= =================== //



    // =================== Nowe Wyswietlanie =================== //

    for(let y = 0; y <= 4; y++){
        // let xs = Math.abs(2 - y);
        // let xf = 4 + Math.abs(2 - y) + 2 * Math.abs(2 - Math.abs(2 - y));
        // console.log(y + " " + xs + "-" + xf);
        for(let x = Math.abs(2 - y); x <= 4 + Math.abs(2 - y) + 2 * Math.abs(2 - Math.abs(2 - y)); x+=2){
            const Y = y * 1.732 * Size;
            const X = x * Size;
            const FinalX = X + AddX;
            const FinalY = Y + AddY;

            // === Dict check === //
            const field = gameState.view.state.board.find(field =>
                field.pos[0] === y &&
                field.pos[1] === x
            );

            let Path: string = "undefined/undefined";
            let Rotation: number = 0;

            if (field) {
                Path = field.unit.faction + "/" + field.unit.name;
                Rotation = field.unit.rotation * 60;
                console.log("{" + y + ", " + x +  "}  " + Path + "     R: " + Rotation);

                // Items.push(
                //     <Image imageName={Path} x={FinalX} y={FinalY} poz1={y} poz2={x} height={((Size * 2 + 15) * 0.866)} rotation={30 + Rotation} gameState={gameState} />
                // )
            }

            let Color: string = "#d3be00";
            const Clickable = gameState.view.availableActions.board.find(Clickable =>
                Clickable[0] === y &&
                Clickable[1] === x
            );
            if(Clickable) Color = "#666666";

            Items.push(
                <Tile imageName={Path} x={FinalX} y={FinalY} poz1={y} poz2={x} size={Size * 2 + 15} rotation={Rotation + 30} color={Color} opacity={0.1} gameState={gameState} sendAction={sendAction} />
            )

            // Items.push(
            //     <Hexagon x={FinalX} y={FinalY} poz1={y} poz2={x} size={Size * 2 + 15} rotation={30} color={Color} opacity={0.5} gameState={gameState} sendAction={sendAction}> {y}, {x} </Hexagon>
            // )
        }
    }




    // Hand //
    const VerticalSpacing = 1.732 * Size;
    // keep whole hex visible
    const LeftX = Size + 10;
    const RightX = ScreenWidth - Size - 10;
    // vertically centered
    const StartY = CenterY - VerticalSpacing;

    for (let i = -1; i <= 3; i+=2) {
        const FinalX = LeftX;
        const FinalY = StartY + i * VerticalSpacing;
        // === Dict check === //
        const Index = (i + 1) / 2;
        const TokenName = gameState.view.state.hands[currentfaction].tokens[Index];
        let Path: string = "undefined/undefined";
        if(TokenName !== undefined) Path = currentfaction + "/" + TokenName;


        Items.push(
            <Tile imageName={Path} x={FinalX} y={FinalY} poz1={Index} poz2={-1} size={Size * 2 + 15} rotation={30} gameState={gameState} sendAction={sendAction} color="#00aaff" opacity={0.1} />
        )
    }
    // const [enemyfaction, setEnemyfaction] = useState(gameState.view.state.factions[0]);
    // if(enemyfaction === currentfaction) setEnemyfaction(gameState.view.state.factions[1]);

    const enemyfaction = 
        gameState.view.state.factions.find((candidate) => candidate !== currentfaction) ??
        gameState.view.state.factions[0];

    // ======= Enemy Hand ======= //
    for( let i = -1; i <= 3; i+=2) {
        const FinalX = RightX;
        const FinalY = StartY + i * VerticalSpacing;
        // === Dict check === //
        const Index = (i + 1) / 2;
        const TokenName = gameState.view.state.hands[enemyfaction].tokens[Index];
        let Path: string = "undefined/undefined";
        if(TokenName !== undefined) Path = enemyfaction + "/" + TokenName;

        Items.push(
            <Tile imageName={Path} x={FinalX} y={FinalY} poz1={Index} poz2={999} size={Size * 2 + 15} rotation={30} gameState={gameState} sendAction={sendAction} color="#00aaff" opacity={0.1} />
        )
    }
    // ======= ========== ======= //
    // ==== //


    // ===== Buttons ===== //
    let ButtonPoz: number = (height / 16);
    let Ile: number = 0;

    for(const Name of gameState.view.availableActions.buttons) {
        console.log("BUTTON: " + Name);
        Items.push(
            <GameButton x={RightX - Size * 2 - 100} y={ButtonPoz + Ile * (height / 20)} height={height / 20} width={height / 8} text={Name} sendAction={sendAction} gameState={gameState} />
        )
        Ile += 1;
    }

    // ===== ======= ===== //

    // ===== Message ===== //
    let Text: string = gameState.view.uiState.message;
    if(Text) {
        Items.push(
            <TextBox x={width / 2} y={ButtonPoz} text={Text} />
        );
    }
    // ===== ======= ===== //

    // ===== Sztaby i stosy ===== //
    const CurrentHeadquarterHP = gameState.view.scores[currentfaction];
    const EnemyHeadquarterHP = gameState.view.scores[enemyfaction];

    const CurrentPile = gameState.view.state.piles[currentfaction];
    const EnemyPile = gameState.view.state.piles[enemyfaction];

    Items.push(
        <div>
            <TextBox x={LeftX} y={height / 32} text={"HP: " + CurrentHeadquarterHP} />
            <TextBox x={RightX} y={height / 32} text={"HP: " + EnemyHeadquarterHP} />
        </div>
    )
    Items.push(
        <div>
            <TextBox x={LeftX} y={height - (height / 32)} text={"Pile size: " + CurrentPile} />
            <TextBox x={RightX} y={height - (height / 32)} text={"Pile size: " + EnemyPile} />
        </div>
    )
    // ===== ============== ===== //

    // console.log("======");
    // console.log(window.api);
    // console.log("======");

    // =================== ================= =================== //

    return (
        <div className="canvas">
            {Items}
        </div>
    )
}
