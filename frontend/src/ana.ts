// useGameSocket.ts
import { useRef, useState, useEffect, useCallback } from "react";
import { createGameSocket, WebSockedMessage } from "./websockets/websocketClient";

export function useGameSocket() {
  const socketReference = useRef<WebSocket | null>(null);
  const [messages, setMessages] = useState<WebSockedMessage[]>([]);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      console.log("No token found");
      return;
    }

    const socket = createGameSocket(token, (message) => {
      setMessages((prev) => [...prev, message]);
    });

    socketReference.current = socket;

    return () => {
      socket.close();
      socketReference.current = null;
    };
  }, []);

  const sendMessage = useCallback((message: WebSockedMessage) => {
    const socket = socketReference.current;

    if (!socket || socket.readyState !== WebSocket.OPEN) {
      console.log("WebSocket is not open");
      return;
    }

    socket.send(JSON.stringify(message));
  }, []);

  return {
    socket: socketReference.current,
    messages,
    sendMessage,
  };
}