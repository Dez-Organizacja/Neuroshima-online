import { useState } from "react";
import Button from "./components/Button";
import TextInput from "./components/TekstInput";
import DisplayText from "./components/DisplayText";
import { Login } from "./features/auth/Login";
import  "./styles/Button.css";
import "./styles/Background.css";
import "./styles/DisplayText.css";
import "./styles/TextInputs.css"; 
type LoginScreenProps = {
    onSwitchToRegister: () => void;
    onAcceptedLogin: () => void;
};

export default function LoginScreen({onSwitchToRegister, onAcceptedLogin} : LoginScreenProps){
    let url = "http://localhost:8080/api/auth/login";
    const [username, setName] = useState("");
    const [password, setPassword] = useState("");
    async function handleLogin() {
    try {
        const data = await Login(username, password, url);
        if (data.token) {
            onAcceptedLogin();  
        } 
        else {
            console.log("Login returned data, but no token");
        }
    } 
    catch (error) {
        console.log("Wrong login");
        if (error instanceof Error) {
            console.log(error.message);
        }
    }
  }
    return(
        <div className="loginBackground">
  <DisplayText className="mainText" text="Login to proceed" />
  <DisplayText className="usernameText" text="Username" />

  <TextInput
    className="usernameInput"
    value={username}
    onChange={setName}
    placeholder="Enter Username"
  />

  <DisplayText className="passwordText" text="Password" />

  <TextInput
    className="passwordInput"
    value={password}
    onChange={setPassword}
    placeholder="Enter Password"
  />

  <Button className="loginButton" onClick={handleLogin} text="Login" />

  <DisplayText
    className="switchToRegisterText"
    text="You don't have an account?"
  />

  <Button
    className="switchButton"
    onClick={onSwitchToRegister}
    text="Register"
  />
</div>
    )
}