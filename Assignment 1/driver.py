import os
import random
import time
from maze import Maze
from astar import astar, gothroughastar, manhattan_distance, is_valid
from backwardastar import gothroughbackwardastar
from binaryheap import BinaryHeap
import copy

def generate_and_save_mazes(num_mazes=50, width=101, height=101, directory="mazes"):
    """Generates and saves mazes to text files, displaying the first one."""

    if not os.path.exists(directory):
        os.makedirs(directory)

    for i in range(num_mazes):
        maze = Maze(width=width, height=height)
        filename = os.path.join(directory, f"maze{i}.txt")
        with open(filename, "w") as file:
            file.write(f"{width} {height}\n")
            for row in maze.grid:
                row_str = "".join(map(str, [1 if cell else 0 for cell in row]))
                file.write(row_str + "\n")

        if i == 0:  # Display the first maze
            print("First Maze Generated:")
            maze.display(astar(1, 1), astar(21, 21))  # Display the first maze
        print(f"Maze {i} saved to {filename}")

def loadMazes(directory="mazes"):
    """Loads mazes from text files."""
    mazes = []
    for filename in os.listdir(directory):
        if filename.startswith("maze") and filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, "r") as file:
                    lines = file.readlines()
                    width, height = map(int, lines[0].split())
                    grid = []
                    for line in lines[1:]:
                        row = [True if cell == '1' else False for cell in line.strip()]
                        grid.append(row)
                    maze = Maze(width=width, height=height)
                    maze.grid = grid
                    mazes.append(maze)
            except FileNotFoundError:
                print(f"Error: File not found - {filepath}")
            except ValueError:
                print(f"Error: Invalid maze format - {filepath}")
    return mazes

def repeated_forward_a_star(maze, start, goal, tie_break):
    grid = [[astar(x, y, maze.grid[y][x] == 1) for x in range(maze.width)] for y in range(maze.height)]
    start_node = grid[start[1]][start[0]]
    goal_node = grid[goal[1]][goal[0]]
    start_time = time.time()
    path, closed_set = gothroughastar(grid, start_node, goal_node, tie_break=tie_break)
    end_time = time.time()
    runtime = end_time - start_time
    return path, len(closed_set), runtime

def repeated_backward_a_star(maze, start, goal, tie_break):
    grid = [[astar(x, y, maze.grid[y][x] == 1) for x in range(maze.width)] for y in range(maze.height)]
    start_node = grid[start[1]][start[0]]
    goal_node = grid[goal[1]][goal[0]]
    start_time = time.time()
    path, closed_set = gothroughbackwardastar(grid, goal_node, start_node, tie_break=tie_break)
    end_time = time.time()
    runtime = end_time - start_time
    return path, len(closed_set), runtime

if __name__ == "__main__":
    # Generate and save 50 mazes, display the first one
    generate_and_save_mazes()

    # --- Test 4: Maze Test (Single Maze for Demonstration) ---
    print("--- Test 4: Maze Test (Single Maze for Demonstration) ---")
    maze = Maze(width=101, height=101)
    start = (20, 20)
    goal = (80, 80)

    print(f"\n start coordinates:  {start}")
    print(f"\n goal coordinates:  {goal}")

    grid_maze_forward = [[astar(x, y, maze.grid[y][x] == 1) for x in range(maze.width)] for y in range(maze.height)]
    grid_maze_backward = copy.deepcopy(grid_maze_forward)
    for row in grid_maze_backward:
        for node in row:
            node.parent = None

    start_node_maze_forward = grid_maze_forward[start[1]][start[0]]
    goal_node_maze_forward = grid_maze_forward[goal[1]][goal[0]]

    start_node_maze_backward = grid_maze_backward[goal[1]][goal[0]]
    goal_node_maze_backward = grid_maze_backward[start[1]][start[0]]

    print("\nMaze before A*:")
    maze.display(astar(start[0], start[1]), astar(goal[0], goal[1]))

    # Forward A*
    start_time = time.time()
    path_maze_forward, closed_set_maze_forward = gothroughastar(grid_maze_forward, start_node_maze_forward, goal_node_maze_forward, tie_break='larger')
    end_time = time.time()
    forward_runtime = end_time - start_time
    forward_expanded = len(closed_set_maze_forward)
    print(f"\nForward A* Expanded Cells: {forward_expanded}")
    print(f"Forward A* Runtime: {forward_runtime:.4f} seconds")
    if path_maze_forward:
        print("Forward Path:", [(node.x, node.y) for node in path_maze_forward])
        print("Path Found: Yes")
    else:
        print("Forward Path: None")
        print("Path Found: No")
        print("Message: No path found.")

    print("\nMaze after Forward A*:")
    maze.display(astar(start[0], start[1]), astar(goal[0], goal[1]), path_maze_forward)

    # Backward A*
    start_time = time.time()
    path_maze_backward, closed_set_maze_backward = gothroughbackwardastar(grid_maze_backward, start_node_maze_backward, goal_node_maze_backward, tie_break='larger')
    end_time = time.time()
    backward_runtime = end_time - start_time
    backward_expanded = len(closed_set_maze_backward)
    print(f"\nBackward A* Expanded Cells: {backward_expanded}")
    print(f"Backward A* Runtime: {backward_runtime:.4f} seconds")
    if path_maze_backward:
        print("Backward Path:", [(node.x, node.y) for node in path_maze_backward])
        print("Path Found: Yes")
    else:
        print("Backward Path: None")
        print("Path Found: No")
        print("Message: No path found.")

    print("\nMaze after Backward A*:")
    maze.display(astar(start[0], start[1]), astar(goal[0], goal[1]), path_maze_backward)

    # Test 5: No Path Test
    maze.grid[goal[1]][goal[0]] = 1
    path_maze, closed_set_maze = gothroughastar(grid_maze_forward, start_node_maze_forward, goal_node_maze_forward, tie_break='larger')
   # if path_maze is None:
       # print("\nastar Test 5 (No Path Maze Test): PASS")
    #else:
       # print("\nastar Test 5 (No Path Maze Test): FAIL")
       # print("Path found when it should not exist:", path_maze)

    # --- Repeated A* Searches (50 Grids) & Analysis ---
    print("\n--- Repeated A* Searches (50 Grids) & Analysis ---")
    mazes = loadMazes()
    tie_breaks = ['larger', 'smaller']

    # Part 2: Tie-Breaking Comparison (Using First Maze)
    print("\nPart 2: Tie-Breaking Comparison (First Maze)")
    maze = mazes[0]
    #start = (1, 1)
    #goal = (21, 21)
    for tie_break in tie_breaks:
        forward_result, forward_expanded, forward_runtime = repeated_forward_a_star(maze, start, goal, tie_break)
        print(f"Forward A* (Tie: {tie_break}) Expanded Cells: {forward_expanded}, Runtime: {forward_runtime:.4f} seconds")

    # Part 3: Forward vs. Backward Comparison (Using First Maze)
    print("\nPart 3: Forward vs. Backward Comparison (First Maze)")
    for tie_break in tie_breaks:
        forward_result, forward_expanded, forward_runtime = repeated_forward_a_star(maze, start, goal, tie_break)
        backward_result, backward_expanded, backward_runtime = repeated_backward_a_star(maze, start, goal, tie_break)
        print(f"Tie Break: {tie_break}")
        print(f"Forward A* Expanded Cells: {forward_expanded}, Runtime: {forward_runtime:.4f} seconds")
        print(f"Backward A* Expanded Cells: {backward_expanded}, Runtime: {backward_runtime:.4f} seconds")

    # Statistical Analysis (50 Grids)
    print("\nStatistical Analysis (50 Grids)")
    total_forward_larger_expanded = 0
    total_forward_smaller_expanded = 0
    total_backward_larger_expanded = 0
    total_backward_smaller_expanded = 0
    total_forward_larger_runtime = 0
    total_forward_smaller_runtime = 0
    total_backward_larger_runtime = 0
    total_backward_smaller_runtime = 0

    for maze in mazes:
        forward_result_larger, forward_expanded_larger, forward_runtime_larger = repeated_forward_a_star(maze, start, goal, 'larger')
        forward_result_smaller, forward_expanded_smaller, forward_runtime_smaller = repeated_forward_a_star(maze, start, goal, 'smaller')
        backward_result_larger, backward_expanded_larger, backward_runtime_larger = repeated_backward_a_star(maze, start, goal, 'larger')
        backward_result_smaller, backward_expanded_smaller, backward_runtime_smaller = repeated_backward_a_star(maze, start, goal, 'smaller')

        total_forward_larger_expanded += forward_expanded_larger
        total_forward_smaller_expanded += forward_expanded_smaller
        total_backward_larger_expanded += backward_expanded_larger
        total_backward_smaller_expanded += backward_expanded_smaller

        total_forward_larger_runtime += forward_runtime_larger
        total_forward_smaller_runtime += forward_runtime_smaller
        total_backward_larger_runtime += backward_runtime_larger
        total_backward_smaller_runtime += backward_runtime_smaller

    # Calculate Averages
    avg_forward_larger_expanded = total_forward_larger_expanded / 50
    avg_forward_smaller_expanded = total_forward_smaller_expanded / 50
    avg_backward_larger_expanded = total_backward_larger_expanded / 50
    avg_backward_smaller_expanded = total_backward_smaller_expanded / 50

    avg_forward_larger_runtime = total_forward_larger_runtime / 50
    avg_forward_smaller_runtime = total_forward_smaller_runtime / 50
    avg_backward_larger_runtime = total_backward_larger_runtime / 50
    avg_backward_smaller_runtime = total_backward_smaller_runtime / 50

    # Output Averages
    print(f"Forward A* (Larger g-values): Avg Expanded Cells: {avg_forward_larger_expanded:.2f}, Avg Runtime: {avg_forward_larger_runtime:.4f} seconds")
    print(f"Forward A* (Smaller g-values): Avg Expanded Cells: {avg_forward_smaller_expanded:.2f}, Avg Runtime: {avg_forward_smaller_runtime:.4f} seconds")
    print(f"Backward A* (Larger g-values): Avg Expanded Cells: {avg_backward_larger_expanded:.2f}, Avg Runtime: {avg_backward_larger_runtime:.4f} seconds")
    print(f"Backward A* (Smaller g-values): Avg Expanded Cells: {avg_backward_smaller_expanded:.2f}, Avg Runtime: {avg_backward_smaller_runtime:.4f} seconds")

    # File Location for the 50 Mazes
    print("\n50 Mazes are saved in the 'mazes' folder in the same directory as this script.")