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
            path_nodes = []
            while current:
                path_nodes.append(current)
                current = current.parent
            path_nodes = path_nodes[::-1]
            path_coordinates = [[node.x, node.y] for node in path_nodes] # Convert to coordinates
            return path_coordinates, closed_set

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = current.x + dx, current.y + dy
            if is_valid(nx, ny, rows, cols) and not grid[ny][nx].is_obstacle:
                neighbor = grid[ny][nx]
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