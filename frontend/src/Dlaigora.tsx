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

type Animation = 
    | {type : "attack"; attacker : [number, number]; target : [number, number];}
    | {type : "wound"; target : [number, number]; wounds : number;}
    | {type : "destroy"; target : [number, number];}
    | {type : "weaken"; target : [number, number]; damage : number;}
    | {type : "set_wire"; target : [number, number]; wired: boolean;}
    | {type : "rotation"; target : [number, number]; rotation : number;}

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
        phase: string
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
        animations : Animation[]
    }
}

function extractGameView(value: unknown): GameState["view"] | null {
  if (typeof value !== "object" || value === null) {
    return null;
  }

  const record = value as Record<string, unknown>;
  const candidate =
    typeof record.view === "object" && record.view !== null
      ? (record.view as Record<string, unknown>)
      : record;

  if (
    typeof candidate.phase !== "string" ||
    typeof candidate.state !== "object" ||
    candidate.state === null ||
    typeof candidate.scores !== "object" ||
    candidate.scores === null
  ) {
    return null;
  }
  return {
    ...candidate,
    animations: Array.isArray(candidate.animations)
      ? candidate.animations
      : [],
  } as GameState["view"];
}

export function useProcesedGameState() {
  const { latestMessage } = useGameSocketContext();
  const [prevGameState, setPrevGameState] = useState<GameState | null>(null);
  const [gameState, setGameState] = useState<GameState | null>(null);

  useEffect(() => {
    if (!latestMessage) {
      return;
    }

    const hasRestoredGameView =
      latestMessage.messageType === "GETROOMSTATUS_RESPONSE" &&
      typeof latestMessage.gameView === "object" &&
      latestMessage.gameView !== null;

    if (
      latestMessage.messageType === "ACTION_RESPONSE" ||
      latestMessage.messageType === "NEWGAME_RESPONSE" ||
      hasRestoredGameView
    ) {
      const view = extractGameView(latestMessage.gameView);
      if (!view) {
        console.error("Server returned an invalid gameView", latestMessage);
        return;
      }

      setGameState((currentGameState) => {
        setPrevGameState(currentGameState);
        return { view };
      });

      if (
        latestMessage.messageType === "NEWGAME_RESPONSE" &&
        typeof latestMessage.createdGameId === "string"
      ) {
        localStorage.setItem("gameId", latestMessage.createdGameId);
      }

      if (
        latestMessage.messageType === "GETROOMSTATUS_RESPONSE" &&
        typeof latestMessage.gameId === "string" &&
        latestMessage.gameId.trim()
      ) {
        localStorage.setItem("gameId", latestMessage.gameId);
      }
      return;
    }

    if (latestMessage.messageType === "ERROR") {
      console.error(latestMessage.error);
    }
  }, [latestMessage]);

  return { gameState, prevGameState };
}