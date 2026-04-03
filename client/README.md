# Prosty program TypeScript z Canvas

Minimalny projekt webowy: TypeScript kompiluje sie do `dist/main.js`, a strona `index.html` wyswietla animacje na `<canvas>`.

## Wymagania

- Node.js 18+

## Jednorazowe uruchomienie

```bash
npm install
npm run build
npm run start
```

Nastepnie otworz: `http://localhost:5173`

## Tryb dev z auto-refresh (run.sh)

Skrypt uruchamia:
- `tsc --watch` (auto-kompilacja TypeScript)
- `browser-sync` (serwer i auto-refresh po zmianach)

```bash
chmod +x ./run.sh
./run.sh
```

Domyslna konfiguracja:
- `HOST=localhost`
- `PORT=5173`
- `OPEN_BROWSER=false`

Przyklad z wlasna konfiguracja:

```bash
HOST=0.0.0.0 PORT=5173 OPEN_BROWSER=true ./run.sh
```

Zatrzymanie: `Ctrl+C`.
