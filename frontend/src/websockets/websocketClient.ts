import { gameWebSocketUrl } from "../config";

export type WebSocketMessage = {
    messageType : string;
    [key: string] : unknown;
}

export function createGameSocket(
    token : string,
    onMessage : (message: WebSocketMessage) => void,
    onOpen?: () => void,
    onClose?: (event: CloseEvent) => void,
    onError?: (event: Event) => void
){
    const url = gameWebSocketUrl(token);
    const socket = new WebSocket(url);

    socket.onopen = () => {
        console.log("WebSocket connected");
        onOpen?.();
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("WebSocket message:", data);
        onMessage(data);
    };

    socket.onerror = (event) => {
        console.log("WebSocket error");
        onError?.(event);
    };

    socket.onclose = (event) => {
        console.log("WebSocket closed");
        onClose?.(event);
    };

    return socket;
}
