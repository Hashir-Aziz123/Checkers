# ♟Checkers AI Game

A classic Checkers game featuring a powerful AI opponent built using **Minimax with Alpha-Beta Pruning**. Challenge yourself across multiple difficulty levels as the AI evaluates deeper into the game tree.

---

## Features

-  Play checkers against an intelligent AI  
-  AI uses Minimax + Alpha-Beta Pruning  
-  Adjustable difficulty via search depth  
-  Legal move highlighting and turn enforcement  
-  Clean, responsive user interface
-  
---

## AI Strategy: Minimax with Alpha-Beta Pruning

The AI is implemented using a custom **Minimax algorithm with Alpha-Beta Pruning** and features several layers of intelligence:

### 💡 Key Components:

- **Transposition Table**: Caches board evaluations to avoid redundant calculations.
- **Capture & King Prioritization**: Move ordering gives priority to high-impact moves.
- **Position-Based Evaluation**: Scores are influenced by piece count, king status, and central control.
- **Mobility Heuristic**: Encourages flexible positioning by rewarding available moves.
- **Random Noise**: Slight randomness prevents predictable patterns in tie scenarios.

### 📊 Difficulty Levels:

| Level   | Description              | Depth |
|---------|--------------------------|-------|
| Easy    | Fast, shallow lookahead  | 1     |
| Medium  | Balanced opponent        | 2     |
| Hard    | Strategic and aggressive | 4     |

The AI evaluates every legal move, simulates it on a copied board, and recursively explores the resulting game states.

