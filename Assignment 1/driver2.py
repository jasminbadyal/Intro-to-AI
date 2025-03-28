import os
from maze import Maze

if __name__ == "__main__":
    maze = Maze()
    maze.display()
    maze.display()
    maze.display()
    maze.save("0.txt")