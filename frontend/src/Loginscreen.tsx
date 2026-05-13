import { useState } from "react";
import Button from "./components/Button";
import TextInput from "./components/TekstInput";
import DisplayText from "./components/DisplayText";
import { Login } from "./features/auth/Login";

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
        <div>
            <DisplayText zawartosc="Username"></DisplayText>
            <TextInput value={username} onChange={setName} placeholder="Enter Username" ></TextInput>
            <DisplayText zawartosc="Password"></DisplayText>
            <TextInput value={password} onChange={setPassword} placeholder="Enter Password"></TextInput>
            <Button onClick={handleLogin} zawartosc="Login"></Button>
            <DisplayText zawartosc="You don't have an account?"></DisplayText>
            <Button onClick={onSwitchToRegister} zawartosc="Register"></Button>
        </div>
    )
}