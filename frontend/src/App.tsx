import { useState } from "react";
import React from "react";
import LoginScreen from "./Loginscreen";
import RegisterScreen from "./Registerscreen";
import MenuScreen from "./Menu";
import HexTest from "./HexTest";
import { RoomScreen } from "./WaitingRoom";
import { GameSocketProvider } from "./websockets/gameSocketContext";

export default function App() {
  const [screen, setScreen] = useState<"login" | "register" | "menu" | "room" | "game">("login");
  function SwitchToLogin(){
    setScreen("login");
  }
  function SwitchToRegister(){
    setScreen("register");
  }
  function SwitchToMenu(){
    setScreen("menu");
  }
  function SwitchToRoom(){
    setScreen("room");
  }
  function SwitchToGame(){
    setScreen("game");
  }
  // function RenderScreen(){
  //   if(screen == "login"){
  //     return <LoginScreen onSwitchToRegister={SwitchToRegister} onAcceptedLogin={SwitchToMenu} />
  //   }
  // }
  return (
    <div>
      {screen === "login" ? (
      <LoginScreen onSwitchToRegister={SwitchToRegister} onAcceptedLogin={SwitchToMenu}></LoginScreen>
    ): screen === "register" ? (
      <RegisterScreen onSwitchToLogin={SwitchToLogin}></RegisterScreen>
    ) : (
      <GameSocketProvider>
      {screen === "menu" ?(
      <MenuScreen onSwitchToWaitingRoom={SwitchToRoom}></MenuScreen>
    ) : screen === "room" ?(
      <RoomScreen onSwitchToGame={SwitchToGame} onSwitchToMenu={SwitchToMenu}></RoomScreen>
    ) : 
     screen === "game" ?(
      <HexTest></HexTest>
    ) : (
      <p>AAAAAA</p>
    )}
     </GameSocketProvider>
    )}
  </div>
  )
}