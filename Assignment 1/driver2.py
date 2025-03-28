import os
from maze import Maze
from astar import gothroughastar

if __name__ == "__main__":
    maze = Maze()
    gothroughastar(maze)
    maze.save("0.txt")