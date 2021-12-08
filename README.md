# Maze-Pathfinder

[![Actions Status](https://img.shields.io/github/actions/workflow/status/boher/Maze-Pathfinder/tests.yml?label=Tests&logo=github&style=flat-square)](https://github.com/boher/Maze-Pathfinder/actions)
![Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue?logo=python&logoColor=white&style=flat-square)
[![License: MIT](https://img.shields.io/badge/License-MIT-darkturquoise.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Maze Generation and Pathfinding Algorithm Visualizer - [Project Basis](https://youtu.be/JtiK0DOeI4A)

## INSTRUCTIONS TO PLAY

### Note: A version of the instructions is also available in-game

- Execution of main.py would open a pygame window with the instructions opened on load
  <br>*Closing the instructions would enable buttons and dropdown menus in the navigation bar*
- User can double-click on any white squares to place the start node (in green), followed by the end node (in red)
- User can add a bomb which dictates the pathfinding algorithm to find the bomb first before looking for the end node
- User can subsequently click and drag on any white squares to construct walls, also known as blocking nodes that can't
  be traversed
- User can click and drag the start node, end node and bomb node to move them across the white squares
  <br>*Note: if pathfinding algorithm has been executed, this action would automatically compute the path*

## Pathfinding Algorithms

> :bellhop_bell: **The condition of placing the start and end node must be satisfied**
>
> Path of traversal is drawn with purple nodes

### Option 1: Dijkstra's

- Weighted
- Shortest path guaranteed

### Option 2: A* Search

- Weighted
- Shortest path guaranteed with admissible heuristics

### Option 3: Greedy Best-First

- Weighted
- Shortest path not guaranteed with admissible heuristics

### Option 4: Breadth First Search

- Unweighted
- Shortest path guaranteed

### Option 5: Depth First Search

- Unweighted
- Shortest path not guaranteed

## Setup Local Development Environment

It is recommended that you [fork the repository on GitHub](https://help.github.com/articles/about-forks) before cloning

After cloning, it is recommended to
[create a virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
using Python version 3.8, 3.9 or 3.10

```bash
# Install external dependencies
pip install -r requirements.txt

# Install in editable (development) mode
pip install -e .
```

To run tests and linter, use the [tox](https://tox.readthedocs.io/en/latest/index.html) testing framework to ensure
compatibility for Python version 3.8, 3.9 and 3.10

```bash
# Install test dependencies
pip install -r requirements_test.txt
```