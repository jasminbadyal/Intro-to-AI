import math
from binaryheap import BinaryHeap

class astar:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = math.inf
        self.h = 0
        self.parent = None

    def f(self):
        return self.g + self.h

    def __lt__(self, other):  # Corrected for min-heap
        return self.f() < other.f()
    
    def __eq__(self, other): # For comparing cells
        return self.x == other.x and self.y == other.y
    
    def __hash__(self): 
        return hash((self.x, self.y))


def manhattan_distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)  


def is_valid(x, y, rows, cols):
    return 0 <= x < rows and 0 <= y < cols


def gothroughastar(grid, start, goal):  
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    open_list = BinaryHeap()  
    closed_set = set()

    start.g = 0
    open_list.push(start)

    while not open_list.is_empty():
        current = open_list.pop()

        if current in closed_set:  
            continue

        closed_set.add(current)  

        if current == goal:  
            path = []
            while current:
                path.append(current)
                current = current.parent
            return path[::-1]

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = current.x + dx, current.y + dy
            if is_valid(nx, ny, rows, cols) and grid[nx][ny] != 1:  
                neighbor = grid[nx][ny]
                tentative_g = current.g + 1

                if tentative_g < neighbor.g:
                    neighbor.parent = current
                    neighbor.g = tentative_g
                    neighbor.h = manhattan_distance(neighbor, goal)

                    if neighbor in open_list:
                        open_list.update(neighbor) 
                    else:
                        open_list.push(neighbor)

    return None