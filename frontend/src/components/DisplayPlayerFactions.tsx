import { imagesByName } from "../Images";

type DisplayPlayerFactionsProps = {
  playerFactions: Record<string, string | null>;
  playersInRoom?: string[];
  hostUsername?: string;
  canManageRoom?: boolean;
  isRoomPolicyBusy?: boolean;
  pendingHostUsername?: string | null;
  onMakeHost?: (player: string) => void;
};

function displayFactionName(faction: string) {
  return faction.charAt(0).toUpperCase() + faction.slice(1);
}

export default function DisplayPlayerFactions({
  playerFactions,
  playersInRoom = Object.keys(playerFactions),
  hostUsername,
  canManageRoom = false,
  isRoomPolicyBusy = false,
  pendingHostUsername = null,
  onMakeHost,
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
        const isHost = Boolean(hostUsername && player === hostUsername);
        const isPendingHost = pendingHostUsername === player;

        return (
          <div
            className={`player-row${isHost ? " is-host" : ""}`}
            key={player}
          >
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
              <span className="player-row__name-line">
                <strong>{player}</strong>
                {isHost ? (
                  <span className="player-row__host-badge">
                    <span aria-hidden="true">◆</span>
                    Host
                  </span>
                ) : canManageRoom && onMakeHost ? (
                  <button
                    className="player-row__host-action"
                    type="button"
                    onClick={() => onMakeHost(player)}
                    disabled={isRoomPolicyBusy}
                    aria-label={`Make ${player} the room host`}
                    title={`Transfer room control to ${player}`}
                  >
                    <span aria-hidden="true">◆</span>
                    {isPendingHost ? "Transferring…" : "Make host"}
                  </button>
                ) : null}
              </span>
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
