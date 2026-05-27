import {useState, useEffect, useContext} from "react";
import Button from "./components/Button";
import TextInput from "./components/TekstInput";
import DisplayText from "./components/DisplayText";
import { useGameSocketContext } from "./websockets/gameSocketContext";
import DisplayStringList from "./components/DisplayStringList"
import DisplayPlayerFactions from "./components/DisplayPlayerFactions"
type RoomScreenProps = {
    onSwitchToGame : () => void;
    onSwitchToMenu : () => void;
}

type PlayerFactions = Record<string, string | null>

function isPlayerFactions(value: unknown): value is PlayerFactions {
    return (
        typeof value === "object" &&
        value !== null &&
        !Array.isArray(value) &&
        Object.values(value).every(
            (faction) => typeof faction === "string" || faction === null
        )
    );
}

export function RoomScreen({onSwitchToGame, onSwitchToMenu} : RoomScreenProps){
    const {latestMessage, setFactionAWFR, leaveRoomAWFR, startNewGameAWFR} = useGameSocketContext();
    const [playersInRoom, setPlayersInRoom] = useState<string[]>([]);
    const [playerFactions, setPlayerFactions] = useState<PlayerFactions>();
    const [currentReply, setCurrentReply] = useState<string>("");
    const factions : string[] = ["borgo", "moloch"];
    const [faction, setFaction] = useState<string>("");
    useEffect(() => {
        if(!latestMessage){
            return ;
        }
        if(latestMessage.messageType == "NEWGAME_RESPONSE" && typeof latestMessage.createdGameId === "string"){
            console.log("New game started");
            localStorage.setItem("gameID", latestMessage.createdGameId);
            onSwitchToGame();
        }
        if(latestMessage.messageType == "GETROOMSTATUS_RESPONSE" &&
            Array.isArray(latestMessage.playersInRoom) &&
                latestMessage.playersInRoom.every((player) => typeof player === "string") &&
                isPlayerFactions(latestMessage.playerFactions)
            ) {
            console.log("Refreshed players")
            setPlayersInRoom(latestMessage.playersInRoom);
            setPlayerFactions(latestMessage.playerFactions)
            if(typeof latestMessage.gameId === "string"){
                onSwitchToGame();
            }
        }

    }, [latestMessage])
    async function HandleFaction(){
        try{
            if(faction != ""){
                const response = await setFactionAWFR(faction);
                if(response.messageType == "SETFACTION_RESPONSE"){
                    if(typeof response.faction == "string" && typeof response.serverStatus == "string"){
                        localStorage.setItem("faction", (response.faction));
                        setCurrentReply(response.serverStatus);
                        console.log("Response ok")
                    }
                    else if(typeof response.error == "string"){
                        setCurrentReply(response.error);
                        console.log("Response not ok")
                    }
                }
                else if (response.messageType === "ERROR") {
                    console.log("Could not set faction:", response.error);
                }
            }
        }
        catch (error) {
            if (error instanceof Error) {
                console.log(error.message);
            }
        }
    }
    async function HandleLeave() {
        // RefreshPlayersInRoom()
        try{
            const response = await leaveRoomAWFR();
            if(response.messageType == "LEAVEROOM_RESPONSE"){
                console.log("Joined room")
                localStorage.removeItem("room")
                onSwitchToMenu();
            }
            else if (response.messageType === "ERROR") {
               console.log("Could not leave room:", response.error);
            }
        } 
        catch (error) {
            if (error instanceof Error) {
                console.log(error.message);
            }
        }
    }
    async function HandleStartGame() {
        // RefreshPlayersInRoom();
        if(playersInRoom.length == 2){
            try{
                const response = await startNewGameAWFR(playersInRoom, factions);
                if(response.messageType == "NEWGAME_RESPONSE" && typeof response.createdGameId === "string"){
                    console.log("New game started");
                    localStorage.setItem("gameID", response.createdGameId);
                    onSwitchToGame();
                    console.log("Could not start game");
                }
                else if (response.messageType === "ERROR"){
                }
            }
            catch (error) {
                if (error instanceof Error) {
                    console.log(error.message);
                }
            }
        }
        else{
            console.log("Players != 2");
        }
    }
    return (
        <div>
            <Button text = "Leave Room" onClick={HandleLeave}></Button>
            {/* <Button text = "Refresh Players" onClick={RefreshPlayersInRoom}></Button> */}
            {/* <DisplayStringList strings={playersInRoom}></DisplayStringList> */}
            <Button text = "Start Game" onClick={HandleStartGame}></Button>
            <DisplayText text = "Select Faction"></DisplayText>
            <Button onClick={() => {setFaction("borgo")}} text = "Borgo"></Button>
            <Button onClick={() => {setFaction("moloch")}} text = "Moloch"></Button>
            <Button onClick={HandleFaction} text = "Confirm"></Button>
            <DisplayText text = "Players and their factions"></DisplayText>
            <DisplayPlayerFactions playerFactions={playerFactions ?? {}}></DisplayPlayerFactions>
            <DisplayText text={currentReply}></DisplayText>
        </div>
    )
}