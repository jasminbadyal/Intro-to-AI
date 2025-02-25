import random
from astar import astar

class Maze:
    def __init__(self, width=101, height=101):
        self.width = width
        self.height = height
        self.grid = [[1 for _ in range(width)] for _ in range(height)]  # Initialize with walls

        self.generate_prim()

    def generate_prim(self):
        start_x, start_y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
        self.grid[start_y][start_x] = 0

        frontier = [(start_x + dx, start_y + dy, start_x, start_y)
                    for dx, dy in [(0, 2), (0, -2), (2, 0), (-2, 0)]
                    if 1 <= start_x + dx < self.width - 1 and 1 <= start_y + dy < self.height - 1]

        while frontier:
            fx, fy, cx, cy = random.choice(frontier)
            frontier.remove((fx, fy, cx, cy))

            if self.grid[fy][fx] == 1:
                self.grid[fy][fx] = 0
                self.grid[(fy + cy) // 2][(fx + cx) // 2] = 0

                frontier += [(fx + dx, fy + dy, fx, fy)
                             for dx, dy in [(0, 2), (0, -2), (2, 0), (-2, 0)]
                             if 1 <= fx + dx < self.width - 1 and 1 <= fy + dy < self.height - 1]

    def display(self, start=None, goal=None, path=None):
        print(" " + "_" * (self.width + 2))
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
        print(" " + "‾" * (self.width + 2))

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

   