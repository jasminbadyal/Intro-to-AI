from os import path
import random


class Maze:
    grid = [[-1 for _ in range(101)] for _ in range(101)]
    
    def __init__(self):
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

        for i in range(101):
            for j in range(101):
                unvisited.add((i, j))

        start_r = random.randint(0, 100)
        start_c  = random.randint(0, 100)
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

    @classmethod
    def load(cls, path:path):
        maze = cls()
        with open(path, "r") as file:
            for i, line in enumerate(file):
                line
                maze.grid[i] = [int(bit) for bit in line.strip()]
        return maze

    def save(self, path:path):
        with open(path, "w") as file:
            for i in range(len(self.grid)):
                line = "".join(map(str, self.grid[i])) + "\n"
                file.write(line)


    def display(self, start:tuple=None, goal:tuple=None, path:list=None):
        print(" " + "_" * 101)

        for r, row in enumerate(self.grid):
            str = "|"
            for c, item in enumerate(row):
                if (r, c) == start:
                    str += "S"
                elif (r, c) == goal:
                    str += "G"
                elif path and (r, c) in path:
                    str += "+"
                elif item == 1:
                    str += "X"
                elif item == 0:
                    str += " "
                elif item == -1:
                    str += "?"
            str += "|"
            print(str)

        print(" " + "‾" * 101)