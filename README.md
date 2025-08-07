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

The AI is built on a depth-limited Minimax search algorithm with Alpha-Beta Pruning for efficiency.

###  Evaluation Function
- Piece count (normal vs king)
- Positional advantage (e.g., center control, edge protection)
- Promotion potential
- Optional: Mobility / move diversity

### 🧮 Difficulty Levels

| Level | Description                | Depth |
|-------|----------------------------|-------|
| Easy  | Basic lookahead            | 2     |
| Medium| Balanced performance       | 4     |
| Hard  | Challenging + aggressive   | 6     |
| Expert| High-depth strategic AI    | 8+    |

