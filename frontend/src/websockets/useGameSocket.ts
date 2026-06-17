import { useRef, useState, useEffect, useCallback, useMemo } from "react";
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
        let disposed = false;
        const token = localStorage.getItem("token");

        if (!token) {
            console.log("No token found");
            return;
        }
        
        const socket = createGameSocket(
            token,
            (serverMessage) => {
                if (disposed) {
                    return;
                }

                if (serverMessage.messageType === "CONNECTION") {
                    const serverRoomId =
                        typeof serverMessage.roomId === "string"
                            ? serverMessage.roomId.trim()
                            : "";

                    // Reconcile browser state with the authoritative server
                    // affiliation before room components issue status requests.
                    if (serverRoomId) {
                        localStorage.setItem("room", serverRoomId);
                    } else {
                        localStorage.removeItem("room");
                        localStorage.removeItem("gameId");
                        localStorage.removeItem("faction");
                    }

                    setIsConnected(true);
                }

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
                // Wait for the server's CONNECTION envelope before exposing
                // the socket as ready. That envelope also carries the
                // authoritative room affiliation used for session reclaim.
            },
            () => {
                if (!disposed) {
                    setIsConnected(false);
                }
            },
            () => {
                if (!disposed) {
                    setIsConnected(false);
                }
            }
        );
        socketReference.current = socket;

        return () => {
            disposed = true;
            pendingRequestsRef.current.forEach((pending) => {
                clearTimeout(pending.timeoutId);
                pending.reject(new Error("WebSocket connection closed"));
            });
            pendingRequestsRef.current = [];
            socket.close();
            socketReference.current = null;
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
    const actions = useMemo(
        () => createGameSocketActions(sendMessage, sendAndWaitForResponse),
        [sendMessage, sendAndWaitForResponse],
    );

return {
    messages,
    latestMessage,
    isConnected,
    sendAndWaitForResponse,
    sendMessage,
    ...actions,
};
}