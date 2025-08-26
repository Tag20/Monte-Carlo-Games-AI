🎮 Monte Carlo Games AI

A collection of classic Python games enhanced with Monte Carlo Tree Search (MCTS) AI.
Play manually, or let the AI agents make decisions in real time.

✨ Games Included

🧩 2048 with MCTS AI (Mcts_2048.py)

Tkinter-based GUI.

Use arrow keys to play.

Press p to let the MCTS AI take over.

👻 Pac-Man with Monte Carlo Ghosts (Pac Man.py)

Turtle graphics version of Pac-Man.

Pac-Man is player-controlled.

Ghosts move using Monte Carlo exploration/exploitation.

🐍 Snake with MCTS Pathfinding (SnakeGame.py)

Built with Pygame.

Snake is controlled by an MCTS-based planner that seeks food and avoids collisions.

❌⭕ Tic-Tac-Toe with MCTS AI (Tic-Tak-Toe-mcts.py)

Uses Ursina engine for 3D-like visuals.

Human plays O, AI plays X.

The AI evaluates moves with Monte Carlo rollouts.

🔴🟡 Connect 4 with MCTS AI (Connect4.py)

Two-player Connect 4 board game.

Human vs MCTS-powered AI.

Graphical board rendering.

🖥️ Main Launcher

Run main.py to launch a simple menu for selecting a game.

No need to run each .py individually.

🛠️ Tech Stack

Python
Tkinter – 2048 GUI
Turtle Graphics – Pac-Man
Pygame – Snake
Ursina – Tic-Tac-Toe
Custom Board Rendering – Connect 4
Monte Carlo Tree Search (MCTS) – AI logic across all games

📂 Project Structure
Monte-Carlo-Games-AI/
│── main.py                # Main launcher menu
│── Mcts_2048.py           # 2048 with MCTS AI (Tkinter GUI)
│── Pac Man.py             # Pac-Man with Monte Carlo Ghosts (Turtle)
│── SnakeGame.py           # Snake with MCTS AI (Pygame)
│── Tic-Tak-Toe-mcts.py    # Tic-Tac-Toe with MCTS AI (Ursina)
│── Connect4.py            # Connect 4 with MCTS AI

🎮 Controls

2048: Arrow keys. Press p to enable AI.
Pac-Man: Arrow keys to move Pac-Man. Ghosts use Monte Carlo AI.
Snake: Runs automatically with MCTS planning.
Tic-Tac-Toe: Click squares to place O. AI plays X.
Connect 4: Click/select a column to drop a piece. AI responds with MCTS move.
