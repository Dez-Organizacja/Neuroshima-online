type IncomingMessageHandler = (payload: unknown) => void;

export class WebsocketHandler {
	private socket: WebSocket | null = null;
	private incomingMessageHandler: IncomingMessageHandler | null = null;

	constructor(private readonly backendBaseUrl: string = "http://localhost:8080") {}

	public async connect(token: string): Promise<void> {
		if (this.socket?.readyState === WebSocket.OPEN) {
			return;
		}

		if (!token.trim()) {
			throw new Error("Token jest wymagany do połączenia WebSocket.");
		}

		const wsUrl = this.buildSocketUrl(token);

		await new Promise<void>((resolve, reject) => {
			const socket = new WebSocket(wsUrl);
			let isSettled = false;

			socket.addEventListener("open", () => {
				isSettled = true;
				resolve();
			});

			socket.addEventListener("error", () => {
				if (!isSettled) {
					reject(new Error("Nie udalo sie nawiazac polaczenia WebSocket."));
				}
			});

			socket.addEventListener("close", (event) => {
				if (!isSettled) {
					reject(
						new Error(
							`Polaczenie WebSocket zostalo zamkniete podczas laczenia (kod ${event.code}).`
						)
					);
				}

				this.socket = null;
			});

			socket.addEventListener("message", (event) => {
				if (!this.incomingMessageHandler) {
					return;
				}

				const rawData = event.data;

				if (typeof rawData !== "string") {
					this.incomingMessageHandler(rawData);
					return;
				}

				try {
					this.incomingMessageHandler(JSON.parse(rawData));
				} catch {
					this.incomingMessageHandler(rawData);
				}
			});

			this.socket = socket;
		});
	}

	public setIncomingMessageHandler(handler: IncomingMessageHandler): void {
		this.incomingMessageHandler = handler;
	}

	public send(payload: string | object): void {
		if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
			throw new Error("WebSocket nie jest polaczony.");
		}

		const serializedPayload =
			typeof payload === "string" ? payload : JSON.stringify(payload);

		this.socket.send(serializedPayload);
	}

	public disconnect(): void {
		this.socket?.close();
		this.socket = null;
	}

	public isConnected(): boolean {
		return this.socket?.readyState === WebSocket.OPEN;
	}

	private buildSocketUrl(token: string): string {
		const baseUrl = new URL(this.backendBaseUrl);

		const protocol =
			baseUrl.protocol === "https:"
				? "wss:"
				: baseUrl.protocol === "http:"
					? "ws:"
					: baseUrl.protocol;

		const wsUrl = new URL("/ws/chat", `${protocol}//${baseUrl.host}`);
		wsUrl.searchParams.set("token", token);

		return wsUrl.toString();
	}
}
