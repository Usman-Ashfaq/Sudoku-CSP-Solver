# 🧩 Sudoku CSP Solver

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A powerful Sudoku solver that treats Sudoku as a **Constraint Satisfaction Problem (CSP)**. This implementation combines **Backtracking Search** with **Forward Checking** and the **Minimum Remaining Values (MRV) heuristic** to solve puzzles efficiently—even the notoriously difficult 17-clue puzzles.

Unlike my basic [sudoku-solver](https://github.com/yourusername/sudoku-solver) (which uses simple backtracking), this project demonstrates advanced AI search techniques for constraint optimization.

## ✨ Features

- **Backtracking Search** - Depth-first search with intelligent backtracking
- **Forward Checking** - Prunes invalid assignments early to reduce search space
- **MRV Heuristic** - Always picks the cell with the fewest legal moves first (fail-first principle)
- **Efficient Constraint Propagation** - Maintains possible values for each empty cell
- **Handles All Difficulties** - From easy puzzles to extreme 17-clue puzzles

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only standard library)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/sudoku-csp-solver.git

# Navigate to project directory
cd sudoku-csp-solver

# Run the solver
python sudoku.py
