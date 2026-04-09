import { WebsocketHandler } from "../WebsocketHandler.js";

type AuthLoginResponse = {
	token?: string;
	error?: string;
};

const loginButtonElement = document.getElementById("login-button");
const loginInputElement = document.getElementById("login");
const passwordInputElement = document.getElementById("password");

if (!(loginButtonElement instanceof HTMLButtonElement)) {
	throw new Error("Nie znaleziono przycisku logowania (login-button/login-button).");
}

if (!(loginInputElement instanceof HTMLInputElement)) {
	throw new Error("Nie znaleziono pola login o id 'login'.");
}

if (!(passwordInputElement instanceof HTMLInputElement)) {
	throw new Error("Nie znaleziono pola hasla o id 'password'.");
}

const loginButton = loginButtonElement;
const loginInput = loginInputElement;
const passwordInput = passwordInputElement;

const statusElement = ensureStatusElement();
const websocketHandler = new WebsocketHandler("http://localhost:8080");

websocketHandler.setIncomingMessageHandler((payload) => {
	console.log("Odebrano wiadomosc WebSocket:", payload);
});

loginButton.addEventListener("click", async (event) => {
	event.preventDefault();

	const username = loginInput.value.trim();
	const password = passwordInput.value;

	if (!username || !password) {
		updateStatus("Uzupelnij login i haslo.", true);
		return;
	}

	loginButton.disabled = true;
	updateStatus("Logowanie...", false);

	try {
		const token = await getAuthToken(username, password);

		updateStatus("Laczenie z WebSocket...", false);
		await websocketHandler.connect(token);

		updateStatus("Polaczono z webapp przez WebSocket.", false);
	} catch (error) {
		const errorMessage =
			error instanceof Error ? error.message : "Nieznany blad podczas laczenia.";

		updateStatus(errorMessage, true);
	} finally {
		loginButton.disabled = false;
	}
});

async function getAuthToken(username: string, password: string): Promise<string> {
	const response = await fetch("http://localhost:8080/api/auth/login", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ username, password }),
	});

	let responseBody: AuthLoginResponse | null = null;

	try {
		responseBody = (await response.json()) as AuthLoginResponse;
	} catch {
		responseBody = null;
	}

	if (!response.ok) {
		throw new Error(
			responseBody?.error ?? `Logowanie nieudane (HTTP ${response.status}).`
		);
	}

	if (!responseBody?.token) {
		throw new Error("Serwer nie zwrocil tokenu logowania.");
	}

	return responseBody.token;
}

function ensureStatusElement(): HTMLParagraphElement {
	const existingElement = document.getElementById("connection-status");

	if (existingElement instanceof HTMLParagraphElement) {
		return existingElement;
	}

	const newStatus = document.createElement("p");
	newStatus.id = "connection-status";
	document.body.appendChild(newStatus);

	return newStatus;
}

function updateStatus(message: string, isError: boolean): void {
	statusElement.textContent = message;
	statusElement.style.color = isError ? "#c62828" : "#2e7d32";
}
