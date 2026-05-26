import { WebSocketMessage } from "./websocketClient";

type SendMessage = (message : WebSocketMessage) => void;

type SendMessageAndWaitForResponse = (
    request : WebSocketMessage,
    expectedTypes : string[],
    timeoutId : number,
) => Promise<WebSocketMessage>;

export function createGameSocketActions(sendMessage : SendMessage, sendAWFR : SendMessageAndWaitForResponse){
    function createRoomAWFR(roomName : string){
        const username = localStorage.getItem("username");
        if(!username){
            throw new Error("No username found");
        }
        return sendAWFR({
            messageType : "CREATENEWROOM_REQUEST",
            roomId : roomName,
            playerName : username,
        },
        ["CREATENEWROOM_RESPONSE", "ERROR"],
        5000
        )
    }
    function joinRoomAWFR(roomName : string){
        const username = localStorage.getItem("username");
        if(!username){
            throw new Error("No username found");
        }
        return sendAWFR({
            messageType: "JOINROOM_REQUEST",
            roomId : roomName,
            playerName: username,
        },
        ["JOINROOM_RESPONSE", "ERROR"],
        5000,
        )
    }
    function leaveRoomAWFR(){
        const username = localStorage.getItem("username");
        const room = localStorage.getItem("room");
        if(!username){
            throw new Error("No username found");
        }
        return sendAWFR({
            messageType : "LEAVEROOM_REQUEST",
            roomId : room,
            playerName : username,
        },
        ["LEAVEROOM_RESPONSE", "ERROR"],
        5000,
        )
    }
    function getRoomStatusAWFR(){
        const username = localStorage.getItem("username");
        const room = localStorage.getItem("room");
        return sendAWFR({
            messageType : "GETROOMSTATUS_REQUEST",
            roomId : room,
        },
        ["GETROOMSTATUS_RESPONSE", "ERROR"],
        5000,
        )
    }
    function startNewGameAWFR(playersInRoom : string[], fractions : string[]){
        const room = localStorage.getItem("room");
        // console.log(fractions);
        // const message : WebSocketMessage = {
        //         messageType : "NEWGAME_REQUEST",
        //         roomId : "abc",
        //         scenario : {
        //             fractions : fractions
        //     }
        // }
        // console.log(JSON.stringify(message));
        return sendAWFR({
            messageType : "NEWGAME_REQUEST",
            roomId : room,
            scenario : {
                fractions : fractions
            }
        },
        ["NEWGAME_RESPONSE", "ERROR"],
        5000,   
    )
    }

    return{
        createRoomAWFR,
        joinRoomAWFR,
        leaveRoomAWFR,
        getRoomStatusAWFR,
        startNewGameAWFR,
    }
}