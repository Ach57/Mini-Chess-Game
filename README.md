# 🧠 Mini-Chess-Game ♟️

A simplified chess game with multiple play modes, including Human vs Human, Human vs AI, and AI vs AI, powered by heuristic evaluation functions and optional alpha-beta pruning.

## 📁 Project Structure
Mini-Chess-Game/
├── main.py                   # Entry point with game menu and logic
├── pieces/                  # Chess piece movement logic
│   ├── king.py
│   ├── queen.py
│   ├── bishop.py
│   ├── knight.py
│   ├── pawn.py
├── Logger/
│   └── mini_chess_logger.py  # Game logging utility
├── heuristics/
│   └── heuristics.py         # Evaluation functions: e0, e1, e2
├── SearchAlgorithm/
│   └── search.py             # Search logic for AI moves
└── ...
