from astar import astar, manhattan_distance, is_valid
from binaryheap import BinaryHeap

def gothroughbackwardastar(grid, start, goal, tie_break='larger'):
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
                    # Corrected heuristic calculation:
                    neighbor.h = manhattan_distance(neighbor, goal) #goal is the original start
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