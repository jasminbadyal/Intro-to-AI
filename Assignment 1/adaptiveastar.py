import os
import random
import time
from astar import astar, manhattan_distance, is_valid
from binaryheap import BinaryHeap
from maze import Maze
from driver import display_maze_with_path

def adaptive_astar(grid, start, goal):
    """Performs Adaptive A* search using a BinaryHeap."""
    h_values = {cell: manhattan_distance(cell, goal) for row in grid for cell in row}
    open_list = BinaryHeap()
    closed_set = set()

    start.g = 0
    start.h = h_values[start]
    open_list.push((start.f(), start))

    while not open_list.is_empty():
        _, current = open_list.pop()

        if current in closed_set:
            continue

        closed_set.add(current)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = current.parent
            path.reverse()

            # Adaptive A*: Update heuristic values
            goal_g = len(path) - 1  # Cost to reach goal
            for node in path:
                h_values[node] = goal_g - manhattan_distance(node, goal)

            return path, closed_set

        x, y = current.x, current.y
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Down, Left, Up
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, len(grid), len(grid[0])) and not grid[ny][nx].is_obstacle:
                neighbor = grid[ny][nx]
                tentative_g = current.g + 1

                if tentative_g < neighbor.g:
                    neighbor.parent = current
                    neighbor.g = tentative_g
                    neighbor.h = h_values[neighbor]
                    priority = neighbor.f()

                    if neighbor in open_list.position_map:
                        open_list.update((priority, neighbor))
                    else:
                        open_list.push((priority, neighbor))

    return None, closed_set  # No path found

if __name__ == "__main__":
    random.seed(42)  # Seed for consistent results

    # Load all existing mazes from the mazes folder
    maze_folder = "../mazes"
    maze_files = [os.path.join(maze_folder, f) for f in os.listdir(maze_folder) if f.endswith(".txt")]

    if not maze_files:
        print(f"No maze files found in {maze_folder}.")
        exit(1)

    total_expanded = 0
    total_runtime = 0
    num_mazes = len(maze_files)

    for maze_file in maze_files:
        maze = Maze()
        maze.load(maze_file)
        start = (1, 1)  # Example start position, adjust as needed
        goal = (maze.width - 2, maze.height - 2)  # Example goal position, adjust as needed

        # Convert maze grid to astar nodes
        grid = [[astar(x, y, is_obstacle=(maze.grid[y][x] == 1)) for x in range(maze.width)] for y in range(maze.height)]

        # Measure runtime and run Adaptive A* from scratch
        start_node = grid[start[1]][start[0]]
        goal_node = grid[goal[1]][goal[0]]
        start_time = time.time()
        path_adaptive, expanded_adaptive = adaptive_astar(grid, start_node, goal_node)
        end_time = time.time()
        runtime_adaptive = end_time - start_time

        # Collect data
        total_expanded += len(expanded_adaptive)
        total_runtime += runtime_adaptive

        # Output results for each maze
        path_length = len(path_adaptive) if path_adaptive else "No Path Found"
        result_adaptive_from_scratch = {
            "Maze": maze_file,
            "Path Length": path_length,
            "Expanded Nodes": len(expanded_adaptive),
            "Runtime": runtime_adaptive
        }
        print(result_adaptive_from_scratch)

    # Statistical Analysis
    avg_expanded = total_expanded / num_mazes
    avg_runtime = total_runtime / num_mazes

    print("\nStatistical Analysis (Adaptive A* on Multiple Mazes)")
    print(f"Average Expanded Nodes: {avg_expanded}")
    print(f"Average Runtime: {avg_runtime:.5f} seconds")

