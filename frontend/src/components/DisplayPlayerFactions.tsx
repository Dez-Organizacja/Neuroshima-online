import { imagesByName } from "../Images";

type DisplayPlayerFactionsProps = {
  playerFactions: Record<string, string | null>;
  playersInRoom?: string[];
};

function displayFactionName(faction: string) {
  return faction.charAt(0).toUpperCase() + faction.slice(1);
}

export default function DisplayPlayerFactions({
  playerFactions,
  playersInRoom = Object.keys(playerFactions),
}: DisplayPlayerFactionsProps) {
  const players = playersInRoom.length
    ? playersInRoom
    : Object.keys(playerFactions);

  if (players.length === 0) {
    return (
      <div className="players-empty">
        <span className="players-empty__hex" aria-hidden="true">
          ?
        </span>
        <strong>No commanders connected</strong>
        <p>Waiting for the room status to update.</p>
      </div>
    );
  }

  return (
    <div className="player-list">
      {players.map((player, index) => {
        const faction = playerFactions[player];
        const factionImage = faction
          ? imagesByName[`${faction}/sztab`]
          : undefined;

        return (
          <div className="player-row" key={player}>
            <span className="player-row__number">0{index + 1}</span>

            <span
              className={`player-row__avatar${faction ? " has-faction" : ""}`}
            >
              {factionImage ? (
                <img src={factionImage} alt="" />
              ) : (
                <span aria-hidden="true">?</span>
              )}
            </span>

            <span className="player-row__identity">
              <strong>{player}</strong>
              <small>
                {faction ? displayFactionName(faction) : "Choosing faction…"}
              </small>
            </span>

            <span
              className={`player-row__state${faction ? " is-confirmed" : ""}`}
            >
              {faction ? "Locked" : "Pending"}
            </span>
          </div>
        );
      })}
    </div>
  );
}
