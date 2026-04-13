# TANK YOU

A retro-style 2D tank shooter built with [Pyxel](https://github.com/kitao/pyxel). Battle through endless randomly-generated levels, destroy enemy tanks, and survive as long as you can.

## Features

- **Procedurally generated levels** — four map chunks are randomly assembled each round
- **Three enemy types**, each with unique stats, AI behavior, and shooting patterns
  - Red: Standard tank with basic projectiles
  - Brown: Shotgun — fires a spread of 6 bullets
  - Green: Sniper — slow but high-damage shots with a visible targeting line
- **Destructible environment** — boxes take damage and break apart
- **Scaling difficulty** — more (and tougher) enemies as levels increase
- **Visual feedback** — screen rumble on hit, health bar animation, dither effects

## Requirements

- Python 3.10+
- [Pyxel](https://github.com/kitao/pyxel)

```
pip install pyxel
```

## How to Run

```
python main.py
```

## Controls

| Input | Action |
|-------|--------|
| Arrow keys / WASD | Move and rotate tank |
| Mouse | Aim |
| Left click | Shoot |
| R | Restart after death |

## Project Structure

```
tankgame/
├── main.py              # Game loop and application entry point
├── tank.py              # Tank, Enemy, and Projectile classes
├── world.py             # Map generation and destructible boxes
├── ui.py                # HUD, crosshair, death/pause screens
└── tank_sprites.pyxres  # Pyxel resource file (sprites, tilemaps, sounds)
```
