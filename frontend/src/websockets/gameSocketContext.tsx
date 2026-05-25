import { createContext, useContext } from "react";
import { useGameSocket } from "./useGameSocket";

type GameSocketContextType = ReturnType<typeof useGameSocket>;
const GameSocketContext = createContext<GameSocketContextType | null>(null);

export function GameSocketProvider({children} : {children: React.ReactNode}){
    const gameSocket = useGameSocket();
    return (
        <GameSocketContext.Provider value={gameSocket}>{children}</GameSocketContext.Provider>
    )
}

export function useGameSocketContext(){
    const context = useContext(GameSocketContext);
    if (!context) {
        throw new Error("useGameSocketContext must be used inside GameSocketProvider");
    }
    return context;
}