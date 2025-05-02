# 🧠 Mini-Chess-Game ♟️

A simplified chess game with multiple play modes, including Human vs Human, Human vs AI, and AI vs AI, powered by heuristic evaluation functions and optional alpha-beta pruning.

## 🎮 Game Modes
1. Player vs Player – Play a match with another human.

2. Player vs AI – Challenge an AI opponent.

3. AI vs Player – Let the AI make the first move.

4. AI vs AI – Watch two AI players battle it out.

5. Exit – Quit the game.

## 🧠 AI Configuration

For AI-enabled modes, you can configure:
Max Time per turn (in seconds)
Max Turns per game

Heuristic Function:
- e0 – Basic material count

- e1 – Positional weighting

- e2 – Advanced strategy (e.g., mobility, king safety)

Alpha-Beta Pruning: Toggle ON/OFF

## 🚀 How to Run

1. Clone the repository:
```bash
git clone https://github.com/your-username/Mini-Chess-Game.git
cd Mini-Chess-Game
```
2. Run the main file:
```bash
python main.py
```
## 📚 Example Interaction
 -------------------------------
|       Mini Game Chess         |
| 1. Player Vs Player           |
| 2. Player Vs AI               |
| 3. AI Vs Player               |
| 4. AI Vs AI                   |
| 5. Exit                       |
 -------------------------------
Please enter a valid option: 2
Max time (seconds): 10
Max turns: 30
Heuristic (e0, e1, e2): e1
Enable Alpha-Beta? (yes/no): yes



