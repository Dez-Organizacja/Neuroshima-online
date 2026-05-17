import { useState } from "react";
import LoginScreen from "./Loginscreen";
import RegisterScreen from "./Registerscreen";



export default function App() {
  const [screen, setScreen] = useState<"login" | "register" | "menu" | "game">("login");
  function SwitchToLogin(){
    setScreen("login");
  }
  function SwitchToRegister(){
    setScreen("register");
  }
  function AcceptedLogin(){
    setScreen("menu");
  }
  function SwitchToGame(){
    setScreen("game");
  }
  function RenderScreen(){
    if(screen == "login"){
      return <LoginScreen onSwitchToRegister={SwitchToRegister} onAcceptedLogin={AcceptedLogin} />
    }
  }
  return (
    <div>
      {screen === "login" ? (
      <LoginScreen onSwitchToRegister={SwitchToRegister} onAcceptedLogin={AcceptedLogin} />
    ) : (
      <RegisterScreen onSwitchToLogin={SwitchToLogin} />
    )}
    </div>
  );
}