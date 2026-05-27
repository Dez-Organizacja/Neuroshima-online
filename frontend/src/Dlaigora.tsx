import { useState, useEffect } from "react";
import { useGameSocketContext } from "./websockets/gameSocketContext";

type BoardCell = {
    pos : [number, number];
    unit : {
        name : string,
        faction : string,
        ROTATION : number,
        DAMAGE : number,
        WIRED : number,
        ability_used : boolean,
    }
}
export type GameState = {
    view : {
        state : {
            factions : [string, string]
            board : BoardCell[]
            hands : {
                [key : string] : {tokens : [string, string, string]}
            }
        }
        avaliableActions : {
            hand : [boolean, boolean, boolean]
            board : [number, number][]
            buttons : string[]
        }
        uiState : {
            faction : string,
            mode : string,
            message : string
        }
    }
}

export function useProcesedGameState(){
    const {latestMessage} = useGameSocketContext();
    const [gameState, setGameState] = useState<GameState | null>(null)
    useEffect(() => {
        if(!latestMessage){
            return;
        }
        if(latestMessage.messageType === "ACTION_RESPONSE" && latestMessage.gameView){   
            setGameState({
                view : latestMessage.gameView as GameState["view"]
            });
        }
        if (latestMessage.messageType === "ERROR") {
            console.error(latestMessage.error);
            return;
        }
    }, [latestMessage]);

    return { gameState};
}