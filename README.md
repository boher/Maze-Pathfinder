# Maze Pathfinding Visualization
![Actions Status](https://github.com/boher/Maze-Pathfinder/actions/workflows/main.yml/badge.svg?branch=main)
[![forthebadge made-with-python](https://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<br>[Project Basis](youtu.be/JtiK0DOeI4A)

## INSTRUCTIONS TO PLAY
- Execution of main.py would open a pygame window, where user can click on any white squares (nodes) to place a start node (in green), followed by an end node (in red)
- User can subsequently click on any white squares to construct walls, also known as blocking nodes that can't be traversed

## Pathfinding Algorithms
### Option 1: Dijkstra's
- As long as the condition of placing a start & end node is satisfied, user can press key '1' to trigger Dijkstra's shortest path
- Turquoise nodes are nodes already traversed (looked at), while blue nodes are nodes in the process of traversing (currently being looked at)
- Dijkstra's shortest path is completed by drawing the weighted path of traversal with purple nodes

### Option 2: A*
- As long as the condition of placing a start & end node is satisfied, user can press key '2' to trigger A* search
- Turquoise nodes are nodes already traversed (looked at), while blue nodes are nodes in the process of traversing (currently being looked at)
- A* search is completed by drawing the informed shortest weighted path of traversal with purple nodes

### Option 3: Greedy Best-First
- As long as the condition of placing a start & end node is satisfied, user can press key '3' to trigger Greedy Best-First search
- Shortest path not guaranteed
- Turquoise nodes are nodes already traversed (looked at), while blue nodes are nodes in the process of traversing (currently being looked at)
- Greedy Best-First search is completed by drawing the weighted path of traversal with purple nodes

### Option 4: BFS
- As long as the condition of placing a start & end node is satisfied, user can press key '4' to trigger Breadth-First search (BFS)
- Shortest path not guaranteed
- Turquoise nodes are nodes already traversed (looked at), while blue nodes are nodes in the process of traversing (currently being looked at)
- BFS is completed by drawing the unweighted path of traversal with purple nodes

### Option 5: DFS
- As long as the condition of placing a start & end node is satisfied, user can press key '5' to trigger Depth-First search (DFS)
- Shortest path not guaranteed
- Turquoise nodes are nodes already traversed (looked at), while blue nodes are nodes in the process of traversing (currently being looked at)
- DFS is completed by drawing the unweighted path of traversal with purple nodes