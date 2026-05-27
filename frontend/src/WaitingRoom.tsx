import {useState, useEffect, useContext} from "react";
import Button from "./components/Button";
import TextInput from "./components/TekstInput";
import DisplayText from "./components/DisplayText";
import { useGameSocketContext } from "./websockets/gameSocketContext";
import DisplayStringList from "./components/DisplayStringList"
type RoomScreenProps = {
    onSwitchToGame : () => void;
    onSwitchToMenu : () => void;
}

export function RoomScreen({onSwitchToGame, onSwitchToMenu} : RoomScreenProps){
    const {latestMessage, leaveRoomAWFR, getRoomStatusAWFR, startNewGameAWFR} = useGameSocketContext();
    const [playersInRoom, setPlayersInRoom] = useState<string[]>([]);
    const factions : string[] = ["borgo", "moloch"];
    
    useEffect(() => {
        if(!latestMessage){
            return ;
        }
        if(latestMessage.messageType == "GETROOMSTATUS_RESPONSE" &&
            Array.isArray(latestMessage.playersInRoom) &&
                latestMessage.playersInRoom.every((player) => typeof player === "string")
            ) {
            console.log("Refreshed players")
            setPlayersInRoom(latestMessage.playersInRoom);
            if(typeof latestMessage.gameId === "string"){
                onSwitchToGame();
            }
        }
    })

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
    // async function RefreshPlayersInRoom() {
    //     try{
    //         const response = await getRoomStatusAWFR();
    //         if(
    //             response.messageType === "GETROOMSTATUS_RESPONSE" &&
    //             Array.isArray(response.playersInRoom) &&
    //             response.playersInRoom.every((player) => typeof player === "string")
    //         ) {
    //             console.log("Refreshed players")
    //             setPlayersInRoom(response.playersInRoom);
    //             if(typeof response.gameId === "string"){
    //                 onSwitchToGame();
    //             }
    //         }
    //         else if (response.messageType === "ERROR") {
    //            console.log("Could not refresh players:", response.error);
    //         }
    //     }
    //     catch (error) {
    //         if (error instanceof Error) {
    //             console.log(error.message);
    //         }
    //     }
    // }
    async function HandleStartGame() {
        // RefreshPlayersInRoom();
        if(playersInRoom.length == 2){
            try{
                const response = await startNewGameAWFR(playersInRoom, factions);
                if(response.messageType == "NEWGAME_RESPONSE" && typeof response.createdGameId === "string"){
                    console.log("New game started");
                    localStorage.setItem("game", response.createdGameId);
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
            <DisplayStringList strings={playersInRoom}></DisplayStringList>
            <Button text = "Start Game" onClick={HandleStartGame}></Button>
        </div>
    )
}