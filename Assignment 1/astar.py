# astar.py
import math
from binaryheap import BinaryHeap

class astar:
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
        if isinstance(other, astar):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __contains__(self, item): 
      if isinstance(item, astar):
        return self.x == item.x and self.y == item.y
      return False

def manhattan_distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def is_valid(x, y, rows, cols):
    return 0 <= x < rows and 0 <= y < cols

def gothroughastar(grid, start, goal, tie_break='larger'):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    open_list = BinaryHeap()
    closed_set = set()

    start.g = 0
    start.h = manhattan_distance(start, goal)
    open_list.push((start.f(), start))

    while not open_list.is_empty():
        _, current = open_list.pop()

        if current in closed_set:
            continue

        closed_set.add(current)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = current.parent
            return path[::-1], closed_set

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = current.x + dx, current.y + dy
            if is_valid(nx, ny, rows, cols) and not grid[ny][nx].is_obstacle: #Corrected grid access
                neighbor = grid[ny][nx] #Corrected grid access
                tentative_g = current.g + 1

                if tentative_g < neighbor.g:
                    neighbor.parent = current
                    neighbor.g = tentative_g
                    neighbor.h = manhattan_distance(neighbor, goal)

                    if tie_break == 'larger':
                        c = rows * cols + 1
                        priority = c * neighbor.f() - neighbor.g
                    else:
                        priority = neighbor.f() + neighbor.g

                    if neighbor in open_list.position_map:
                        open_list.update((priority, neighbor))
                    else:
                        open_list.push((priority, neighbor))

    return None, closed_set