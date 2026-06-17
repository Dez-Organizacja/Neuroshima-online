const FACTION_STORAGE_KEY = "faction";

function readStoredFaction(): string {
  if (typeof window === "undefined") {
    return "";
  }

  return window.localStorage.getItem(FACTION_STORAGE_KEY)?.trim() ?? "";
}

let currentFaction = readStoredFaction();

export function setCurrentFaction(faction: string): void {
  const normalizedFaction = faction.trim();
  currentFaction = normalizedFaction;

  if (typeof window === "undefined") {
    return;
  }

  if (normalizedFaction) {
    window.localStorage.setItem(FACTION_STORAGE_KEY, normalizedFaction);
  } else {
    window.localStorage.removeItem(FACTION_STORAGE_KEY);
  }
}

export function getCurrentFaction(): string {
  if (currentFaction) {
    return currentFaction;
  }

  currentFaction = readStoredFaction();
  return currentFaction;
}

export function clearCurrentFaction(): void {
  setCurrentFaction("");
}
