import os
import random
import time
from maze import Maze
from astar import astar, gothroughastar, manhattan_distance, is_valid
from backwardastar import gothroughbackwardastar
from binaryheap import BinaryHeap
import copy

def repeated_forward_a_star(maze, start, goal, tie_break):
    print(f"Forward A* Start: {start}, Goal: {goal}")
    grid = [[astar(x, y, maze.grid[y][x] == 1) for x in range(maze.width)] for y in range(maze.height)]
    start_node = grid[start[1]][start[0]]
    goal_node = grid[goal[1]][goal[0]]
    start_time = time.time()
    path, closed_set = gothroughastar(grid, start_node, goal_node, tie_break=tie_break)
    end_time = time.time()
    runtime = end_time - start_time
    return path, closed_set, runtime

def repeated_backward_a_star(maze, start, goal, tie_break):
    print(f"Backward A* Start: {start}, Goal: {goal}")
    grid = [[astar(x, y, maze.grid[y][x] == 1) for x in range(maze.width)] for y in range(maze.height)]
    start_node = grid[start[1]][start[0]]
    goal_node = grid[goal[1]][goal[0]]
    start_time = time.time()
    path, closed_set = gothroughbackwardastar(grid, goal_node, start_node, tie_break=tie_break)
    end_time = time.time()
    runtime = end_time - start_time
    return path, closed_set, runtime

def display_maze_with_path(maze, start, goal, path=None, closed_set=None):
    """Displays the maze with the path and closed set marked."""
    maze_copy = copy.deepcopy(maze)
    if path:
        for node in path:
            maze_copy.grid[node.y][node.x] = 2  # Mark path with 2
    if closed_set:
        for node in closed_set:
            if maze_copy.grid[node.y][node.x] != 2: #To not overwrite the path.
                maze_copy.grid[node.y][node.x] = 3 #Mark closed set with 3
    maze_copy.display(start, goal)

def generate_maze_grid_string(maze, start, goal, path=None):
    """Generates a string representation of the maze grid."""
    maze_copy = copy.deepcopy(maze)
    if path:
        for node in path:
            maze_copy.grid[node.y][node.x] = 2  # Mark path with 2
    return maze_copy.display_as_string(start, goal, path)

if __name__ == "__main__":
    random.seed(42)  # Seed for consistent results

    maze_data = []
    if not os.path.exists("mazes"):
        os.makedirs("mazes")

    for i in range(50):
        maze = Maze()
        start = (random.randint(1, maze.width - 2), random.randint(1, maze.height - 2))
        goal = (random.randint(1, maze.width - 2), random.randint(1, maze.height - 2))
        maze.grid[goal[1]][goal[0]] = 0  # Ensure goal is open

        maze_data.append((maze, start, goal))
        maze.save(f"mazes/maze{i}.txt")

    # --- Test 4: Maze Test (Single Maze for Demonstration) ---
    print("--- Test 4: Maze Test (Single Maze for Demonstration) ---")
    first_maze, first_start, first_goal = maze_data[0]
    print(f"Start: {first_start}, Goal: {first_goal}")

    # Display Original Maze
    print("Original Maze:")
    display_maze_with_path(first_maze, first_start, first_goal)

    # Forward A*
    forward_path, forward_closed_set, forward_runtime = repeated_forward_a_star(first_maze, first_start, first_goal, 'larger')
    print(f"Forward A* Path: {[(node.x, node.y) for node in forward_path]}")
    display_maze_with_path(first_maze, first_start, first_goal, forward_path)
    print(f"Forward A* Expanded Cells: {len(forward_closed_set)}, Runtime: {forward_runtime:.4f} seconds")

    # Backward A*
    backward_path, backward_closed_set, backward_runtime = repeated_backward_a_star(first_maze, first_start, first_goal, 'larger')
    print(f"Backward A* Path: {[(node.x, node.y) for node in backward_path]}")
    display_maze_with_path(first_maze, first_start, first_goal, backward_path)
    print(f"Backward A* Expanded Cells: {len(backward_closed_set)}, Runtime: {backward_runtime:.4f} seconds")

    # --- Maze Files ---
    for i, (maze, start, goal) in enumerate(maze_data):
        if i == 0:
            continue
        filename = os.path.join("mazes", f"maze{i}.txt")
        with open(filename, "w") as file:
            file.write(f"Maze {i} - Start: {start}, Goal: {goal}\n\n")

            # Original Maze
            file.write("Original Maze:\n")
            file.write(generate_maze_grid_string(maze, start, goal))
            file.write("\n")

            # Forward A*
            forward_path, forward_closed_set, forward_runtime = repeated_forward_a_star(maze, start, goal, 'larger')
            file.write("Forward A* Path:\n")
            file.write(generate_maze_grid_string(maze, start, goal, forward_path))
            file.write(f"Forward A* Expanded Cells: {len(forward_closed_set)}, Runtime: {forward_runtime:.4f} seconds\n\n")

            # Backward A*
            backward_path, backward_closed_set, backward_runtime = repeated_backward_a_star(maze, start, goal, 'larger')
            file.write("Backward A* Path:\n")
            file.write(generate_maze_grid_string(maze, start, goal, backward_path))
            file.write(f"Backward A* Expanded Cells: {len(backward_closed_set)}, Runtime: {backward_runtime:.4f} seconds\n\n")

    # --- Statistical Analysis (50 Grids) ---
print("\nStatistical Analysis (50 Grids)")
total_forward_larger_expanded = 0
total_forward_smaller_expanded = 0
total_backward_larger_expanded = 0
total_backward_smaller_expanded = 0
total_forward_larger_runtime = 0
total_forward_smaller_runtime = 0
total_backward_larger_runtime = 0
total_backward_smaller_runtime = 0

for maze, start, goal in maze_data:
    forward_result_larger, forward_closed_set_larger, forward_runtime_larger = repeated_forward_a_star(maze, start, goal, 'larger')
    forward_result_smaller, forward_closed_set_smaller, forward_runtime_smaller = repeated_forward_a_star(maze, start, goal, 'smaller')
    backward_result_larger, backward_closed_set_larger, backward_runtime_larger = repeated_backward_a_star(maze, start, goal, 'larger')
    backward_result_smaller, backward_closed_set_smaller, backward_runtime_smaller = repeated_backward_a_star(maze, start, goal, 'smaller')

    # Accumulate results INSIDE the loop
    total_forward_larger_expanded += len(forward_closed_set_larger)
    total_forward_smaller_expanded += len(forward_closed_set_smaller)
    total_backward_larger_expanded += len(backward_closed_set_larger)
    total_backward_smaller_expanded += len(backward_closed_set_smaller)

    total_forward_larger_runtime += forward_runtime_larger
    total_forward_smaller_runtime += forward_runtime_smaller
    total_backward_larger_runtime += backward_runtime_larger
    total_backward_smaller_runtime += backward_runtime_smaller

# Calculate Averages (OUTSIDE the loop, after accumulation)
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

# --- Test 5: Maze Test (Single Maze for Demonstration) ---
print("--- Test 4: Maze Test (Single Maze for Demonstration) ---")
maze = Maze(width=10, height=10)
start = (1, 1)
goal = (4, 4)

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
maze.display(start, goal) #Pass start and goal coordinates.

    #Generate path
forward_path, forward_closed_set = gothroughastar(grid_maze_forward, start_node_maze_forward, goal_node_maze_forward, 'larger')
backward_path, backward_closed_set_backward = gothroughbackwardastar(grid_maze_backward, start_node_maze_backward, goal_node_maze_backward, 'larger')

print('\n Maze with Forward Path:')
maze.display(start, goal, forward_path)

print('\n Maze with Backward Path:')
maze.display(start, goal, backward_path)