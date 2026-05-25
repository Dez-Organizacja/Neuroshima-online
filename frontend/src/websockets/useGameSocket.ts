import { useRef, useState, useEffect, useCallback } from "react";
import { createGameSocket, type WebSocketMessage } from "./websocketClient";
import { createGameSocketActions } from "./gameSocketActions";

type PendingRequest = {
    expectedTypes: string[];
    resolve: (message: WebSocketMessage) => void;
    reject: (error: Error) => void;
    timeoutId: number;
};

export function useGameSocket() {
    const socketReference = useRef<WebSocket | null>(null);

    const [messages, setMessages] = useState<WebSocketMessage[]>([]);
    const [latestMessage, setLatestMessage] = useState<WebSocketMessage | null>(
    null
);  

    const [isConnected, setIsConnected] = useState(false);
    const pendingRequestsRef = useRef<PendingRequest[]>([]);
    useEffect(() => {
        const token = localStorage.getItem("token");

        if (!token) {
            console.log("No token found");
            return;
        }
        
        const socket = createGameSocket(
            token,
            (serverMessage) => {
                setLatestMessage(serverMessage);
                setMessages((previousMessages) => [...previousMessages, serverMessage]);
                const matchingRequest = pendingRequestsRef.current.find((pending) =>
                pending.expectedTypes.includes(serverMessage.messageType)
                );

                if (matchingRequest) {
                    clearTimeout(matchingRequest.timeoutId);    
                    pendingRequestsRef.current = pendingRequestsRef.current.filter(
                        (pending) => pending !== matchingRequest
                    );
                    matchingRequest.resolve(serverMessage);
                }
            },
            () => {
            setIsConnected(true);
            },
            () => {
            setIsConnected(false);
            },
            () => {
            setIsConnected(false);
            }
        );
        socketReference.current = socket;

        return () => {
            socket.close();
            socketReference.current = null;
            setIsConnected(false);
        };
    }, []);

    const sendMessage = useCallback((message: WebSocketMessage) => {
        const socket = socketReference.current;

        if (!socket || socket.readyState !== WebSocket.OPEN) {
            console.log("WebSocket is not open");
            return;
        }

        socket.send(JSON.stringify(message));
    }, []);
    const sendAndWaitForResponse = useCallback((
            request: WebSocketMessage,
            expectedTypes: string[],
            timeoutMs = 5000
        ): Promise<WebSocketMessage> => {
            return new Promise((resolve, reject) => {
            const socket = socketReference.current;

            if (!socket || socket.readyState !== WebSocket.OPEN) {
                reject(new Error("WebSocket is not open"));
                return;
            }
            const timeoutId = window.setTimeout(() => {
                pendingRequestsRef.current = pendingRequestsRef.current.filter(
                (pending) => pending.timeoutId !== timeoutId
                );
                reject(new Error("Server response timed out"));
            }, timeoutMs);
            pendingRequestsRef.current.push({
                expectedTypes,
                resolve,
                reject,
                timeoutId,
            });

            socket.send(JSON.stringify(request));
            });
        },[]
        );
    const actions = createGameSocketActions(sendMessage, sendAndWaitForResponse);

return {
    messages,
    latestMessage,
    isConnected,
    sendAndWaitForResponse,
    sendMessage,
    ...actions,
};
}