import math
import random
import matplotlib
from binaryheap import BinaryHeap
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Node:
    def __init__(self, x, y, is_obstacle=False):
        self.x = x
        self.y = y
        self.g = math.inf
        self.h = 0
        self.parent = None
        self.is_obstacle = is_obstacle
        self.search_id = 0

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
    return 0 <= x < cols and 0 <= y < rows

def repeated_astar_forward(grid, start, goal):
    """
    Implements Repeated Forward A* based on the provided pseudocode, using BinaryHeap.
    Outputs all paths in path_history.
    """

    rows = len(grid)
    cols = len(grid[0])
    start_node = grid[start[1]][start[0]]
    goal_node = grid[goal[1]][goal[0]]
    current_node = start_node
    counter = 0
    path_history = []
    final_path = []
    agent_path = [start]  # Initialize agent path with the start node
    path_history.append(agent_path[:])

    for row in grid:
        for node in row:
            node.search_id = 0

    while current_node != goal_node:
        counter += 1
        goal_node.g = math.inf
        goal_node.search_id = counter

        open_list = BinaryHeap()
        closed_set = set()

        current_node.g = 0
        current_node.search_id = counter

        open_list.push((current_node.f(), current_node))

        while not open_list.is_empty():
            current_f, current = open_list.pop()

            if current_f >= goal_node.g:
                break

            closed_set.add(current)

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = current.x + dx, current.y + dy
                if is_valid(nx, ny, rows, cols) and not grid[ny][nx].is_obstacle:
                    neighbor = grid[ny][nx]
                    if neighbor.search_id < counter:
                        neighbor.g = math.inf
                        neighbor.search_id = counter

                    if neighbor.g > current.g + 1:
                        neighbor.g = current.g + 1
                        neighbor.parent = current
                        neighbor.h = manhattan_distance(neighbor, goal_node)

                        if neighbor in open_list.position_map:
                            open_list.update((neighbor.f(), neighbor))
                        else:
                            open_list.push((neighbor.f(), neighbor))

        path_nodes = []
        temp_node = goal_node
        while temp_node != current_node:
            path_nodes.append(temp_node)
            if temp_node.parent is None:
                break
            temp_node = temp_node.parent

        path_nodes.append(current_node)
        path_nodes.reverse()
        path = [(node.x, node.y) for node in path_nodes]

        if goal_node.g != math.inf:
            final_path = path

            if len(path) > 1:
                next_move = path[1]
                next_node = grid[next_move[1]][next_move[0]]
                current_node = next_node
            else:
                current_node = goal_node
        else:
            if len(path) > 1:
                next_move = path[1]
                next_node = grid[next_move[1]][next_move[0]]
                if not next_node.is_obstacle:
                    current_node = next_node

        agent_path.append((current_node.x, current_node.y))
        path_history.append(agent_path[:])
        print(f"Path added to history: {agent_path}")

    return path_history, final_path
#
def animate(grid, path_history, final_path, start, goal):
    fig, ax = plt.subplots()

    def update(frame):
        ax.clear()
        ax.imshow(grid, cmap='binary', interpolation='nearest')
        ax.plot(start[0], start[1], 'gs', markersize=10)
        ax.plot(goal[0], goal[1], 'rs', markersize=10)

        # Display the agent's position at the current frame
        if frame < len(path_history):
            current_path = path_history[frame]
            if len(current_path) > 0:
                current_position = current_path[-1]  # Get the last position in the path
                ax.plot(current_position[0], current_position[1], 'bo', markersize=5)  # Plot the agent's position
                if frame > 0:
                    previous_path = path_history[frame - 1]
                    if len(previous_path)>0:
                        previous_position = previous_path[-1]
                        # Change color for each new path segment
                        if frame % 2 == 0:
                            line_color = 'b-' # Blue for even frames
                        else:
                            line_color = 'g-' # Green for odd frames
                        ax.plot([previous_position[0], current_position[0]],[previous_position[1], current_position[1]],line_color, linewidth = 2)

        if final_path:
            x_coords, y_coords = zip(*final_path)
            ax.plot(x_coords, y_coords, 'r-', linewidth=2)

    ani = animation.FuncAnimation(fig, update, frames=len(path_history), interval=500, repeat=False)
    plt.show(block=True)

class Maze:
    grid = [[0] * 1 for _ in range(1)]
    width = 0
    height = 0

    def __init__(self, width=20, height=20):  # Set default maze size
        def get_unvisited_neighbors(r:int, c:int):
            neighbors = []
            if r != 0 and (r - 1, c) in unvisited:
                neighbors.append((r - 1, c))
            if r != len(self.grid) - 1 and (r + 1, c) in unvisited:
                neighbors.append((r + 1, c))
            if c != 0 and (r, c - 1) in unvisited:
                neighbors.append((r, c - 1))
            if c != len(self.grid[0]) - 1 and (r, c + 1) in unvisited:
                neighbors.append((r, c + 1))
            return neighbors

        def fill(r:int, c:int):
            if random.random() < 0.7:
                self.grid[r][c] = 0
                stack.append((r, c))
            else:
                self.grid[r][c] = 1

        self.width = width
        self.height = height
        self.grid = [[-1 for _ in range(width)] for _ in range(height)]
        unvisited = set()
        stack = []

        for i in range(height):
            for j in range(width):
                unvisited.add((i, j))

        start_r = random.randint(0, height - 1)
        start_c  = random.randint(0, width - 1)
        unvisited.remove((start_r, start_c))
        stack.append((start_r, start_c))

        while unvisited:
            while stack:
                r, c = stack[-1]
                unvisited_neighbors = get_unvisited_neighbors(r, c)
                if unvisited_neighbors:
                    new_r, new_c = random.choice(unvisited_neighbors)
                    unvisited.remove((new_r, new_c))
                    fill(new_r, new_c)
                else:
                    if self.grid[r][c] == -1:
                        fill(r, c)
                    stack.pop()

            if not unvisited:
                break
            r, c = unvisited.pop()
            fill(r, c)
            stack.append((r, c))

    def get_binary_grid(self):
        binary_grid = [[1 if cell == 1 else 0 for cell in row] for row in self.grid]
        return binary_grid

if __name__ == "__main__":
    maze = Maze()
    integer_grid = maze.get_binary_grid()

    rows = len(integer_grid)
    cols = len(integer_grid[0])
    node_grid = [[Node(x, y, integer_grid[y][x] == 1) for x in range(cols)] for y in range(rows)]

    start = (2, 2)
    goal = (15, 15)

    path_history, final_path = repeated_astar_forward(node_grid, start, goal)

    print("Path History:", path_history)
    print("Final Path:", final_path)

    animate(integer_grid, path_history, final_path, start, goal)