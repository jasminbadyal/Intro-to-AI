import random
import time

from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import numpy as np

class Maze:
    grid = [[0] * 1 for _ in range(1)] 
    width = 0
    height = 0

    def __init__(self, width=101, height=101):
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

        # start and goal
        self.grid[random.randint(0, 100)][random.randint(0, 100)] = 2
        self.grid[random.randint(0, 100)][random.randint(0, 100)] = 3

        # display init
        self.fig, self.ax = plt.subplots(figsize=(10, 10))

        cmap = ListedColormap(["white", "#c2c2c2", "red", "green", "blue"])
        bounds = [0, 1, 2, 3, 4, 5]
        norm = BoundaryNorm(bounds, cmap.N)

        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.xaxis.set_label_position("top")
        self.ax.xaxis.tick_top()
        self.im = self.ax.imshow(np.array(self.grid), cmap=cmap, norm=norm)

        self.plt_shown = False

    @classmethod
    def display_static(cls, grid, start=None, goal=None, path_latest=None):
        while path_latest.parent:
            path_latest = path_latest.parent
        print("grid:",grid)
        print(" " + "_" * len(grid[0]))
        for y in range(len(grid)):
            row_str = "|"
            for x in range(len(grid[0])):
                if start and (x, y) == start:
                    row_str += "S"
                elif goal and (x, y) == goal:
                    row_str += "G"
                elif path_latest and [x, y] in path_latest:
                    row_str += "·"
                elif grid[y][x] == 1:
                    row_str += "X"
                else:
                    row_str += " "
            row_str += "|"
            print(row_str)
        print(" " + "‾" * len(grid[0]))

    def display(self, start=None, goal=None, path=None):
        if not self.plt_shown:
            plt.ion()
            plt.pause(0.5)
            self.plt_shown = True
        else:
            self.im.set_data(np.array(self.grid))
            self.fig.canvas.draw_idle()
            self.fig.canvas.flush_events()
            time.sleep(0.5)

    def display_as_string(self, start=None, goal=None, path=None):
        grid_str = ""
        for y in range(self.height):
            row_str = ""
            for x in range(self.width):
                if start and (x, y) == start:
                    row_str += "S"
                elif goal and (x, y) == goal:
                    row_str += "G"
                elif self.grid[y][x] == 2:  # Check for grid value 2 (path)
                    row_str += "·"  # Mark path
                elif self.grid[y][x] == 1:
                    row_str += "X"
                else:
                    row_str += " "
            grid_str += row_str + "\n"
        return grid_str

    @classmethod
    def load(cls, path_to_file):
        maze = cls()
        with open(path_to_file, "r") as file:
            lines = file.readlines()
            lines = lines[1:len(lines) - 1]

            maze.height = len(lines)
            maze.width = len(lines[0]) - 3

            maze.grid = [[-1 for _ in range(maze.width)] for _ in range(maze.height)]

            for i in range(len(lines)):
                if (i == 0 or i == maze.height):
                    pass
                maze.grid[i] = [1 if char == 'X' else 0 for char in lines[i][1:-2]]
                 
        return maze

    def save(self, path_to_file):
        def mapFunc(x:int):
            if x:
                return "X"
            else:
                return " "
            
        with open(path_to_file, "w") as file:
            file.write(" " + "_" * self.width + "\n")
            for row in self.grid:
                file.write("|" + "".join(map(mapFunc, row)) + "|\n")
            file.write(" " + "‾" * self.width)

# Example usage to print a maze:
if __name__ == "__main__":
    maze = Maze()  # Create a new maze
    maze.display()  # Display the maze
    maze.save("mazes/0.txt")
    maze_again = Maze.load("mazes/0.txt")
    maze_again.display()