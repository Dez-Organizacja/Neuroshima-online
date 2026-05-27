export default function DisplayPlayerFactions({ playerFactions }: {
  playerFactions: Record<string, string | null>;
}) {
  return (
    <div>
      {Object.entries(playerFactions).map(([player, faction]) => (
        <div key={player}>
          {player}: {faction ?? "none"}
        </div>
      ))}
    </div>
  );
}