export type WebSockedMessage = {
    messageType : string;
    [key: string] : unknown;
}
export function createGameSocket(
    token : string,
    onMessage : (message: WebSockedMessage) => void,
    onOpen?: () => void,
    onClose?: () => void,
    onError?: () => void
){
    let url = `ws://localhost:8080/ws/chat?token=${encodeURIComponent(token)}`
    const socket = new WebSocket(url)
    socket.onopen = () => {
    console.log("WebSocket connected");
        onOpen?.();
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("WebSocket message:", data);
        onMessage(data);
    };

    socket.onerror = () => {
        console.log("WebSocket error");
        onError?.();
    };
    socket.onclose = () => {
        console.log("WebSocket closed");
        onClose?.();
    };
    return socket;
}