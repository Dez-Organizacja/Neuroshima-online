import { useState } from "react";
import Button from "./components/Button";
import TextInput from "./components/TekstInput";
import DisplayText from "./components/DisplayText";
import { Register } from "./features/auth/Register";

type RegisterScreenProps = {
    onSwitchToLogin: () => void;
};

export default function RegisterScreen({onSwitchToLogin} : RegisterScreenProps){
    let url = "http://localhost:8080/api/auth/register";
    const [username, setName] = useState("");
    const [password, setPassword] = useState("");
    async function HandleRegister(){
        const data = await Register(username, password, url);
        onSwitchToLogin();
    }
    return(
        <div className="loginBackground">
          <DisplayText className="mainText" text="Create an account" />
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
        
          <Button className="loginButton" onClick={HandleRegister} text="Create account" />
        
          <DisplayText
            className="switchToRegisterText"
            text="You already have an account"
          />
        
          <Button
            className="switchButton"
            onClick={onSwitchToLogin}
            text="Login"
          />
        </div>
    )
}