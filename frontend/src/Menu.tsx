import {useState} from "react";
import Button from "./components/Button";
import TextInput from "./components/TekstInput";
import DisplayText from "./components/DisplayText";
import { useGameSocketContext } from "./websockets/gameSocketContext";

type MenuScreenProps = {
    onSwitchToWaitingRoom : () => void
}

export default function MenuScreen({onSwitchToWaitingRoom} : MenuScreenProps){
    // const gameSocket = useGameSocketContext();
    // console.log("gameSocket context:", gameSocket);
    const [joinRoomName, setJoinRoomName] = useState("");
    const [createRoomName, setCreateRoomName] = useState("");
    
    const {createRoomAWFR, joinRoomAWFR} = useGameSocketContext();
    async function HandleJoin() {
        try{
            const response = await joinRoomAWFR(joinRoomName);
            if(response.messageType == "JOINROOM_RESPONSE"){
                console.log("Joined room")
                localStorage.setItem("room", joinRoomName);
                onSwitchToWaitingRoom();

            }
            else if (response.messageType === "ERROR") {
               console.log("Could not join room:", response.error);
            }
        } 
        catch (error) {
            if (error instanceof Error) {
                console.log(error.message);
            }
        }
    }
    async function HandleCreate() {
        try{
            console.log("Creating Room")
            const response = await createRoomAWFR(createRoomName);
            if(response.messageType == "CREATENEWROOM_RESPONSE"){
                console.log("Created room")
                localStorage.setItem("room", createRoomName);
                onSwitchToWaitingRoom();
            }
            else if (response.messageType === "ERROR") {
               console.log("Could not create room:", response.error);
            }
        } 
        catch (error) {
            if (error instanceof Error) {
                console.log(error.message);
            }
        }
    }
    return (
        <div>
            <DisplayText text="Enter room name to join room"></DisplayText>
            <TextInput value={joinRoomName} onChange={setJoinRoomName} placeholder="Enter room name"></TextInput>
            <Button onClick={() => HandleJoin()} text="Join room"></Button>
            <DisplayText text="Enter room name to create room"></DisplayText>
            <TextInput value={createRoomName} onChange={setCreateRoomName} placeholder="Enter room name"></TextInput>
            <Button onClick={() => HandleCreate()} text="Create room"></Button>
        </div>
    )
}