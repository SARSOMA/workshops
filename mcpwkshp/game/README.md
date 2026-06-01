# 🎮 Super MCP

A single-file, Mario-style HTML quiz game built for the MCP workshop warm-up.
Smash `?` blocks to answer MCP trivia, stomp Goombas for bonus points, and
reach the flag to trigger a fireworks-lit victory.

## Run it

Just open the file in a modern browser:

```powershell
start .\index.html
```

Or serve it locally so audio + canvas behave consistently across browsers:

```powershell
# Python
python -m http.server 8080
# then visit http://localhost:8080/

# or Node
npx serve .
```

## Controls

| Action | Keys |
|---|---|
| Move | ← / → or A / D |
| Jump | Space / ↑ / W |
| Mute music | M |
| Answer (in question modal) | 1 – 4 or click |

Touch controls appear automatically on small screens.

## How to score

- Smash a `?` block → answer correctly: **+100 score, +1 coin**
- Stomp a Goomba (land on its head): **+50 score**
- Touch a Goomba from the side or get a wrong answer: **−1 life**
- Reach the flag → flag descends the pole, fireworks light up the sky 🎆

## Customize

Everything lives in `index.html`. Likely edit spots:

1. **Questions** — `const QUESTIONS = [ ... ]` near the top of the `<script>`.
   Each entry is `{ q, choices: [...], a: <index> }`.
2. **Level layout** — `const LEVEL_ROWS = [ ... ]`. All rows must be exactly
   the same length. Tile legend:
   - `.` empty &nbsp; `G` ground &nbsp; `B` brick &nbsp; `Q` question block
   - `P` pipe (2×2, anchored at top-left) &nbsp; `F` flag &nbsp; `C` cloud
3. **Enemy spawns** — `const ENEMY_SPAWNS = [ ... ]` (tile column × direction).

## Audio

Music and SFX are synthesized live with the Web Audio API — an original
chiptune composition (melody + walking bass + arp), no external assets and
no third-party samples. Browsers require a user gesture before audio plays,
which is why music starts after you click **START**.

