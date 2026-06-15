let currentFaction = "";

export function setCurrentFaction(faction: string): void {
  currentFaction = faction;
}

export function getCurrentFaction(): string {
  return currentFaction;
}