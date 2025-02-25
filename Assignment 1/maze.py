import random
from astar import astar

class Maze:
    grid = [[-1 for _ in range(101)] for _ in range(101)]
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

    def display(self, start=None, goal=None, path=None):
        print(" " + "_" * self.width)
        for y in range(self.height):
            row_str = "|"
            for x in range(self.width):
                if start and (x, y) == start:
                    row_str += "S"
                elif goal and (x, y) == goal:
                    row_str += "G"
                elif path and any((node.x, node.y) == (x, y) for node in path):
                    row_str += "."  # Mark path
                elif self.grid[y][x] == 1:
                    row_str += "X"
                else:
                    row_str += " "
            row_str += "|"
            print(row_str)
        print(" " + "‾" * self.width)

    def display_as_string(self, start=None, goal=None, path=None):
        grid_str = ""
        for y in range(self.height):
            row_str = ""
            for x in range(self.width):
                if start and (x, y) == start:
                    row_str += "S"
                elif goal and (x, y) == goal:
                    row_str += "G"
                elif path and any((node.x, node.y) == (x, y) for node in path):
                    row_str += "."  # Mark path
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
            maze.height = len(lines)
            maze.width = len(lines[0].strip()) if lines else 0
            maze.grid = [[int(bit) for bit in line.strip()] for line in lines]
        return maze

    def save(self, path_to_file):
        with open(path_to_file, "w") as file:
            for row in self.grid:
                file.write("".join(map(str, row)) + "\n")

# Example usage to print a maze:
if __name__ == "__main__":
        random.seed(42)  # Add this line to seed the random number generator
        maze = Maze()  # Create a new maze
        maze.display()  # Display the maze

   