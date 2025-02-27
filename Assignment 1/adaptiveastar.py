import random
from astar import astar, manhattan_distance
from binaryheap import BinaryHeap
from maze import Maze

class AdaptiveAStarFromScratch:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.h_values = {cell: manhattan_distance(cell, self.goal) for row in grid for cell in row}

    def search(self):
        """Performs Adaptive A* search using a BinaryHeap."""
        open_list = BinaryHeap()
        closed_set = set()

        self.start.g = 0
        self.start.h = self.h_values[self.start]
        open_list.push((self.start.f(), self.start))

        while not open_list.is_empty():
            _, current = open_list.pop()

            if current in closed_set:
                continue

            closed_set.add(current)

            if current == self.goal:
                path = []
                while current:
                    path.append(current)
                    current = current.parent
                path.reverse()

                # Adaptive A*: Update heuristic values
                goal_g = len(path) - 1  # Cost to reach goal
                for node in path:
                    self.h_values[node] = goal_g - manhattan_distance(node, self.goal)

                return path, closed_set

            x, y = current.x, current.y
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Down, Left, Up
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid):  # Valid grid bounds
                    neighbor = self.grid[ny][nx]
                    if neighbor.is_obstacle:
                        continue

                    tentative_g = current.g + 1  # Uniform movement cost

                    if tentative_g < neighbor.g:
                        neighbor.parent = current
                        neighbor.g = tentative_g
                        neighbor.h = self.h_values[neighbor]
                        priority = neighbor.f()

                        if neighbor in open_list.position_map:
                            open_list.update((priority, neighbor))
                        else:
                            open_list.push((priority, neighbor))

        return None, closed_set  # No path found

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)

    # Generate a consistent random maze for testing
    maze = Maze(width=10, height=10)
    start = astar(0, 0)  # Top-left corner
    goal = astar(9, 9)  # Bottom-right corner

    # Convert maze grid to astar nodes
    grid = [[astar(x, y, is_obstacle=(maze.grid[y][x] == 1)) for x in range(10)] for y in range(10)]

    # Run Adaptive A* from scratch
    adaptive_astar_solver = AdaptiveAStarFromScratch(grid, start, goal)
    path_adaptive, expanded_adaptive = adaptive_astar_solver.search()

    # Output results
    path_length = len(path_adaptive) if path_adaptive else "No Path Found"
    result_adaptive_from_scratch = {
        "Path Length": path_length,
        "Expanded Nodes": len(expanded_adaptive)
    }

    print(result_adaptive_from_scratch)
