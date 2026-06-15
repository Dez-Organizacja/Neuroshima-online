export type RegistrationPayload = {
    username : string,
    password : string,
    captchaId? : string, 
    captchaAnswer? : string,
}

type ApiError = {
    error? : string,
}

export async function Register(payload : RegistrationPayload, url : string) {
    const response = await fetch(url, {
        method : "POST",
        headers : {
            "Content-Type" : "application/json",
        },
        body : JSON.stringify(payload)
    })
    const data = (await response.json().catch(() => ({}))) as ApiError & Record<string, unknown>;
    if(!response.ok){
        throw new Error(data.error || "Registration failed");
    }
    return data;
}