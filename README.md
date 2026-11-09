# Puissance 4 (Connect Four) - Python & Tkinter

A fully playable, visually styled implementation of the classic **Connect Four** game, built entirely in Python using `tkinter` for the graphical interface. 

This project features two distinct game modes included in the repository:
1. **Human vs. Human:** Play locally with a friend.
2. **Human vs. Computer:** Face off against a **Minimax game engine** equipped with Alpha-Beta pruning.

## Features
* **Custom Styled UI:** A modern, neon-themed graphical interface using `tkinter.Canvas`.
* **Minimax Search Engine:** The computer uses a depth-6 recursive search with Alpha-Beta pruning to evaluate board states efficiently.
* **Heuristic Evaluation:** The engine scores the board based on 2-in-a-rows, 3-in-a-rows, center control, and future unplayable threats.
* **Play as Player 1 or 2:** Includes a "Let computer start" option to test the engine's opening moves.
* **Smart Move Generation:** The algorithm prioritizes moves in the center columns where winning combinations are statistically highest.

## Prerequisites
* ![Python](https://img.shields.io/badge/python-3.x-blue)
* ![Tkinter](https://img.shields.io/badge/GUI-tkinter-green) (Standard Python interface to the Tk GUI toolkit, usually included with Python).

## How to Run
1. Clone this repository or download the files.
2. Open your terminal or command prompt.
3. Run the desired game mode:

**For the AI Version (Human vs Computer):**
```bash
python game_ai.py
```
**For the Local Version (Human vs Human):**
```bash
python gamr_pvp.py
```

## How it Works
* **The Search:** It simulates possible moves for both the Computer and the Human up to 6 moves deep.
* **The Heuristic (eval_B):** When it reaches the end of its search, it scores the board using a sliding window technique (checking all 69 possible 4-in-a-row lines). It awards points for building 2s, 3s, and controlling the middle column.
* **Threat Detection (scale):** It scans for lines of 3 and applies heavy bonuses/penalties for threats that are currently blocked but could become dangerous later.
* **Alpha-Beta Pruning:** It skips evaluating branches of the decision tree that are already proven to be worse than previously found moves, allowing it to search deeper without lagging the game.

