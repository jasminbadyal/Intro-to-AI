"""""
if __name__ == "__main__":
    # --- Standalone A* Test Cases ---
    print("--- Standalone A* Test Cases ---")
    # Test Grid (simple 5x5)
    grid_data = [
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ]

    # Create grid of astar objects
    grid_test = [[astar(x, y, grid_data[x][y] == 1) for y in range(5)] for x in range(5)]

    # Test 1: Simple Path
    start_node_test = grid_test[0][0]
    goal_node_test = grid_test[4][4]
    path_test, closed_set_test = gothroughastar(grid_test, start_node_test, goal_node_test, tie_break='larger')

    if path_test:
        print("astar Test 1 (Simple Path): PASS")
    else:
        print("astar Test 1 (Simple Path): FAIL")

    # Test 2: No Path (Block the path)
    grid_test[2][2].is_obstacle = True  # Block the center
    path_test, closed_set_test = gothroughastar(grid_test, start_node_test, goal_node_test, tie_break='larger')

    if path_test is None:
        print("astar Test 2 (No Path): PASS")
    else:
        print("astar Test 2 (No Path): FAIL")

    # Test 3: Smaller tie break
    grid_test[2][2].is_obstacle = False  # Unblock the center
    path_test, closed_set_test = gothroughastar(grid_test, start_node_test, goal_node_test, tie_break='smaller')

    if path_test:
        print("astar Test 3 (Smaller tie break): PASS")
    else:
        print("astar Test 3 (Smaller tie break): FAIL")

    # Test 4: Maze Test
    maze = Maze(width=21, height=21)  # Create a maze
    start = (1, 1)  # Start at (1, 1)
    goal = (19, 19)  # Goal at (19, 19)

    # Create grid of astar objects from the maze
    grid_maze = [[astar(x, y, maze.grid[y][x] == 1) for x in range(maze.width)] for y in range(maze.height)]
    start_node_maze = grid_maze[start[1]][start[0]]
    goal_node_maze = grid_maze[goal[1]][goal[0]]

    print("Maze before A*:")
    maze.display()
    path_maze, closed_set_maze = gothroughastar(grid_maze, start_node_maze, goal_node_maze, tie_break='larger')
    print("Maze after A*:")
    maze.display()

  # Test 5: No Path in Maze Test
    maze.grid[goal[1]][goal[0]] = 1  # Block the goal
    path_maze, closed_set_maze = gothroughastar(grid_maze, start_node_maze, goal_node_maze, tie_break='larger')

    if path_maze is None:
        print("astar Test 5 (No Path Maze Test): PASS")
    else:
        print("astar Test 5 (No Path Maze Test): FAIL")
        print("Path found when it should not exist:", path_maze) #Added print statement.

    # --- Repeated A* Searches ---
    print("\n--- Repeated A* Searches ---")
    mazes = loadMazes()
    maze = mazes[0]  # Use the first maze for testing
    start = (0, 0)
    goal = (100, 100)

    tie_breaks = ['larger', 'smaller']

    print("Part 2: Tie-Breaking Comparison")
    for tie_break in tie_breaks:
        forward_result, forward_expanded = repeated_forward_a_star(maze, start, goal, tie_break)
        print(f"Forward A* (Tie: {tie_break}) Expanded Cells: {forward_expanded}")

    print("\nPart 3: Forward vs. Backward Comparison")
    for tie_break in tie_breaks:
        forward_result, forward_expanded = repeated_forward_a_star(maze, start, goal, tie_break)
        backward_result, backward_expanded = repeated_backward_a_star(maze, start, goal, tie_break)

        print(f"Tie Break: {tie_break}")
        print(f"Forward A* Expanded Cells: {forward_expanded}")
        print(f"Backward A* Expanded Cells: {backward_expanded}")

  """

import os
import random
from maze import Maze
from astar import astar, gothroughastar, manhattan_distance, is_valid
from backwardastar import gothroughbackwardastar
from binaryheap import BinaryHeap
import copy

def loadMazes():
    mazes = []
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    for i in range(50):
        file = os.path.join(parent_dir, f"mazes/{i}.txt")
        if os.path.exists(file):
            mazes.append(Maze.load(file))
        else:
            raise FileNotFoundError(f"Missing {file}")
    return mazes

def repeated_forward_a_star(maze, start, goal, tie_break):
    grid = [[astar(x, y, maze.grid[y][x] == 1) for x in range(maze.width)] for y in range(maze.height)]
    start_node = grid[start[1]][start[0]]
    goal_node = grid[goal[1]][goal[0]]
    path, closed_set = gothroughastar(grid, start_node, goal_node, tie_break=tie_break)
    return path, len(closed_set)

def repeated_backward_a_star(maze, start, goal, tie_break):
    grid = [[astar(x, y, maze.grid[y][x] == 1) for x in range(maze.width)] for y in range(maze.height)]
    start_node = grid[start[1]][start[0]]
    goal_node = grid[goal[1]][goal[0]]
    path, closed_set = gothroughbackwardastar(grid, goal_node, start_node, tie_break=tie_break) #Swapped start and goal
    return path, len(closed_set)

if __name__ == "__main__":
    # ... (Standalone A* Test Cases - unchanged) ...

    # Test 4: Maze Test
    maze = Maze(width=21, height=21)  # Create a maze with 5x5 dimensions

    start = (1, 1)
    goal = (19, 19)

    # Create grid of astar objects from the maze
    grid_maze_forward = [[astar(x, y, maze.grid[y][x] == 1) for x in range(maze.width)] for y in range(maze.height)]
    grid_maze_backward = copy.deepcopy(grid_maze_forward) # Create a deep copy for backward

    start_node_maze_forward = grid_maze_forward[start[1]][start[0]]
    goal_node_maze_forward = grid_maze_forward[goal[1]][goal[0]]

    start_node_maze_backward = grid_maze_backward[goal[1]][goal[0]] #Swapped for backward
    goal_node_maze_backward = grid_maze_backward[start[1]][start[0]] #Swapped for backward

    print("Maze before A*:")
    maze.display(astar(start[0], start[1]), astar(goal[0], goal[1])) #Pass astar objects

    path_maze_forward, closed_set_maze_forward = gothroughastar(grid_maze_forward, start_node_maze_forward, goal_node_maze_forward, tie_break='larger')
    forward_expanded = len(closed_set_maze_forward)
    print(f"Forward A* Expanded Cells: {forward_expanded}")
    if path_maze_forward:
        print("Forward Path:", [(node.x, node.y) for node in path_maze_forward])
    else:
        print("Forward Path: None")


    print("\nMaze after Forward A*:")
    maze.display(astar(start[0], start[1]), astar(goal[0], goal[1]), path_maze_forward) #Pass astar objects

    path_maze_backward, closed_set_maze_backward = gothroughbackwardastar(grid_maze_backward, start_node_maze_backward, goal_node_maze_backward, tie_break='larger')
    backward_expanded = len(closed_set_maze_backward)
    print(f"Backward A* Expanded Cells: {backward_expanded}")
    if path_maze_backward:
        print("Backward Path:", [(node.x, node.y) for node in path_maze_backward])
    else:
        print("Backward Path: None")


    print("\nMaze after Backward A*:")
    maze.display(astar(start[0], start[1]), astar(goal[0], goal[1]), path_maze_backward) #Pass astar objects

    # Test 5: No Path in Maze Test
    maze.grid[goal[1]][goal[0]] = 1  # Block the goal
    path_maze, closed_set_maze = gothroughastar(grid_maze_forward, start_node_maze_forward, goal_node_maze_forward, tie_break='larger')

    if path_maze is None:
        print("\nastar Test 5 (No Path Maze Test): PASS")
    else:
        print("\nastar Test 5 (No Path Maze Test): FAIL")
        print("Path found when it should not exist:", path_maze)

    # --- Repeated A* Searches ---
    print("\n--- Repeated A* Searches ---")
    mazes = loadMazes()
    maze = mazes[0]  # Use the first maze for testing
    start = (0, 0)
    goal = (100, 100)

    tie_breaks = ['larger', 'smaller']

    print("Part 2: Tie-Breaking Comparison")
    for tie_break in tie_breaks:
        forward_result, forward_expanded = repeated_forward_a_star(maze, start, goal, tie_break)
        print(f"Forward A* (Tie: {tie_break}) Expanded Cells: {forward_expanded}")

    print("\nPart 3: Forward vs. Backward Comparison")
    for tie_break in tie_breaks:
        forward_result, forward_expanded = repeated_forward_a_star(maze, start, goal, tie_break)
        backward_result, backward_expanded = repeated_backward_a_star(maze, start, goal, tie_break)

        print(f"Tie Break: {tie_break}")
        print(f"Forward A* Expanded Cells: {forward_expanded}")
        print(f"Backward A* Expanded Cells: {backward_expanded}")

