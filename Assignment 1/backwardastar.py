import math
from binaryheap import BinaryHeap

# Backward A*

class backwardastar:
    def __init__(self, x, y, is_obstacle=False):
        self.x = x
        self.y = y
        self.g = math.inf
        self.h = 0
        self.parent = None
        self.is_obstacle = is_obstacle

    def f(self):
        return self.g + self.h

    def __lt__(self, other):
        return self.f() < other.f()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

def manhattan_distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def is_valid(x, y, rows, cols):
    return 0 <= x < rows and 0 <= y < cols

def gothroughbackwardastar(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    open_list = BinaryHeap()
    closed_set = set()

    goal.g = 0  # Start from the goal, so its g-value is 0
    open_list.push((goal.f(), goal))  # Push goal into open list

    while not open_list.is_empty():
        _, current = open_list.pop()

        if current in closed_set:
            continue

        closed_set.add(current)

        if current == start:  # Goal is to reach the start
            path = []
            while current:
                path.append(current)
                current = current.parent
            return path[::-1], closed_set

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = current.x + dx, current.y + dy
            if is_valid(nx, ny, rows, cols) and not grid[nx][ny].is_obstacle:
                neighbor = grid[nx][ny]
                tentative_g = current.g + 1

                if tentative_g < neighbor.g:
                    neighbor.parent = current
                    neighbor.g = tentative_g
                    neighbor.h = manhattan_distance(neighbor, start)  # Heuristic to start

                    if neighbor in [item[1] for item in open_list.heap]:
                        # Update priority in the heap
                        new_heap = BinaryHeap()
                        for priority, item in open_list.heap:
                            if item == neighbor:
                                new_heap.push((neighbor.f(), neighbor))
                            else:
                                new_heap.push((priority, item))
                        open_list.heap = new_heap.heap
                        open_list._heapify_down(0)

                    else:
                        open_list.push((neighbor.f(), neighbor))

    return None, closed_set

# Example Usage and Testing
if __name__ == "__main__":
    # Create a simple grid (0: free, 1: obstacle)
    grid_data = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 1],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 0]
    ]

    # Create a grid of astar objects.
    grid = [[backwardastar(x, y, grid_data[x][y] == 1) for y in range(len(grid_data[0]))] for x in range(len(grid_data))]

    # Define start and goal positions
    start_x, start_y = 0, 0
    goal_x, goal_y = 4, 4

    start_node = grid[start_x][start_y]
    goal_node = grid[goal_x][goal_y]

    # Run Backward A*
    path, closed_set = gothroughbackwardastar(grid, start_node, goal_node)

    if path:
        print("Path found (Backward A*):")
        for node in path:
            print(f"({node.x}, {node.y})")

        # Visualize the path on the grid (optional)
        visual_grid = [row[:] for row in grid_data]
        for node in path:
            visual_grid[node.x][node.y] = 'P'

        print("\nVisualized Path:")
        for row in visual_grid:
            print(row)

        print("\nClosed Set:")
        for node in closed_set:
            print(f"({node.x}, {node.y})")

    else:
        print("No path found.")
        print("\nClosed Set:")
        for node in closed_set:
            print(f"({node.x}, {node.y})")