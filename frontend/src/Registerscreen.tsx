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
    }
    return(
        <div>
            <DisplayText zawartosc="Username"></DisplayText>
            <TextInput value={username} onChange={setName} placeholder="Enter Username" ></TextInput>
            <DisplayText zawartosc="Password"></DisplayText>
            <TextInput value={password} onChange={setPassword} placeholder="Enter Password"></TextInput>
            <Button onClick={() => Register(username, password, url)} zawartosc="Register"></Button>
            <DisplayText zawartosc="Already have an account?"></DisplayText>
            <Button onClick={onSwitchToLogin} zawartosc="Login"></Button>
        </div>
    )
}