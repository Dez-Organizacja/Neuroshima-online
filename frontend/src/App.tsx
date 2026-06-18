import { useCallback, useState } from "react";
import LoginScreen from "./Loginscreen";
import RegisterScreen from "./Registerscreen";
import MenuScreen from "./Menu";
import Display from "./BoardBoss";
import { RoomScreen } from "./WaitingRoom";
import { GameSocketProvider } from "./websockets/gameSocketContext";

type Screen = "login" | "register" | "menu" | "room" | "game";

const SESSION_KEYS = [
  "token",
  "tokenExpiresAt",
  "username",
  "clientID",
  "room",
  "gameId",
  "faction",
] as const;

function clearStoredSession() {
  SESSION_KEYS.forEach((key) => localStorage.removeItem(key));
}

function hasUsableStoredToken(): boolean {
  const token = localStorage.getItem("token");
  if (!token) {
    return false;
  }

  const expiresAt = localStorage.getItem("tokenExpiresAt");
  if (!expiresAt) {
    clearStoredSession();
    return false;
  }

  const expirationTime = Date.parse(expiresAt);
  if (!Number.isFinite(expirationTime) || expirationTime <= Date.now()) {
    clearStoredSession();
    return false;
  }

  return true;
}

function getInitialScreen(): Screen {
  if (!hasUsableStoredToken()) {
    return "login";
  }

  return localStorage.getItem("room") ? "room" : "menu";
}

export default function App() {
  const [screen, setScreen] = useState<Screen>(getInitialScreen);

  const switchToLogin = useCallback(() => {
    setScreen("login");
  }, []);

  const switchToRegister = useCallback(() => {
    setScreen("register");
  }, []);

  const switchToMenu = useCallback(() => {
    setScreen("menu");
  }, []);

  const switchToRoom = useCallback(() => {
    setScreen("room");
  }, []);

  const switchToGame = useCallback(() => {
    setScreen("game");
  }, []);

  return (
    <div>
      {screen === "login" ? (
        <LoginScreen
          onSwitchToRegister={switchToRegister}
          onAcceptedLogin={switchToMenu}
        />
      ) : screen === "register" ? (
        <RegisterScreen onSwitchToLogin={switchToLogin} />
      ) : (
        <GameSocketProvider>
          {screen === "menu" ? (
            <MenuScreen onSwitchToWaitingRoom={switchToRoom} />
          ) : screen === "room" ? (
            <RoomScreen
              onSwitchToGame={switchToGame}
              onSwitchToMenu={switchToMenu}
            />
          ) : (
            <Display
              onSwitchToWaitingRoom={switchToRoom}
              onSwitchToMenu={switchToMenu}
            />
          )}
        </GameSocketProvider>
      )}
    </div>
  );
}
