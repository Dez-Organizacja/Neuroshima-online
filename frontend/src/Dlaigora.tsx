import { useState, useEffect } from "react";
import { useGameSocketContext } from "./websockets/gameSocketContext";

type BoardCell = {
    pos : [number, number];
    unit : {
        name : string,
        faction : string,
        rotation : number,
        damage : number,
        wounds: number,
        wired : boolean,
        ability_used : boolean,
    }
}
export type GameState = {
    view : {
        state : {
            factions : [string, string]
            board : BoardCell[]
            hands : {
                [key : string] : {tokens : string[]}
            }
            piles : {
                [key: string] : number
            }
        }
        scores : {
            [key : string] : number
        }
        winner : string
        availableActions : {
            hand : boolean[]
            board : [number, number][]
            buttons : string[]
        }
        uiState : {
            faction : string,
            mode : string,
            message : string
        }
        LastClickedHex : {
            source : string,
            pos : [number, number],
            slot : number
        }
    }
}

// export function useProcesedGameState(){
//     const {latestMessage} = useGameSocketContext();
//     const [gameState, setGameState] = useState<GameState | null>(null)
//     useEffect(() => {
//         if(!latestMessage){
//             return;
//         }
//         if(latestMessage.messageType === "ACTION_RESPONSE" && latestMessage.gameView){   
//             setGameState({
//                 view : latestMessage.gameView as GameState["view"]
//             });
//         }
//         if(latestMessage.messageType === "NEWGAME_RESPONSE" && latestMessage.gameView){
//             setGameState({
//                 view : latestMessage.gameView as GameState["view"]
//             })
//             if(typeof latestMessage.createdGameId === "string"){
//                 localStorage.setItem("gameId", latestMessage.createdGameId);
//             }
//             return;
//         }
//         if (latestMessage.messageType === "ERROR") {
//             console.error(latestMessage.error);
//             return;
//         }
//     }, [latestMessage]);

//     return { gameState};
// }

export function useProcesedGameState(){
    const {latestMessage} = useGameSocketContext();
    const [prevGameState, setPrevGameState] = useState<GameState | null>(null);
    const [gameState, setGameState] = useState<GameState | null>(null);
    useEffect(() => {
        if(!latestMessage){
            return;
        }
        if(latestMessage.messageType === "ACTION_RESPONSE" && latestMessage.gameView){
            setPrevGameState(gameState);   
            setGameState({
                view : latestMessage.gameView as GameState["view"]
            });
        }
        if(latestMessage.messageType === "NEWGAME_RESPONSE" && latestMessage.gameView){
            setGameState({
                view : latestMessage.gameView as GameState["view"]
            })
            if(typeof latestMessage.createdGameId === "string"){
                localStorage.setItem("gameId", latestMessage.createdGameId);
            }
            return;
        }
        if (latestMessage.messageType === "ERROR") {
            console.error(latestMessage.error);
            return;
        }
    }, [latestMessage]);

    return {gameState, prevGameState};
}