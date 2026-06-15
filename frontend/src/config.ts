const trimTrailingSlash = (value : string) => value.replace(/\/+$/, "");
const normalizePath = (path : string): string => path.startsWith("/") ? path : `/${path}`;

export function apiUrl(path : string) : string {
    const normalizedPath = normalizePath(path);

    const configuredBase = (import.meta.env.VITE_API_BASE_URL as string | undefined)?.trim();
    if(configuredBase){
        return `${trimTrailingSlash(configuredBase)}${normalizedPath}`;
    }
    if(import.meta.env.DEV){
        return `http://localhost:8080${normalizedPath}`;
    }
    return normalizedPath;
}

export function gameWebSocketUrl(token: string): string {
    
    const configuredBase = (import.meta.env.VITE_WS_BASE_URL as string | undefined)?.trim();

    let base : string;

    if(configuredBase){
        base = configuredBase
    }
    else if (import.meta.env.DEV){
        base = "ws://localhost:8080";
    }
    else{
        const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
        base = `${protocol}//${window.location.host}`;
    }
    return `${base}/ws/chat?token=${encodeURIComponent(token)}`;
}