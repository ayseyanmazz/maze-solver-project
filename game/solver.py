from collections import deque
import time


def get_open_neighbors(matrix, cell):
    r, c = cell
    rows = len(matrix)
    cols = len(matrix[0])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []

    for dr, dc in directions:
        nr = r + dr
        nc = c + dc

        if 0 <= nr < rows and 0 <= nc < cols:
            if matrix[nr][nc] == 0:
                neighbors.append((nr, nc))

    return neighbors


def build_path(parent, target):
    path = []
    current = target

    while current is not None:
        path.append(current)
        current = parent.get(current)

    path.reverse()
    return path


def build_alternative_paths(parent, visited, shortest_path):
    shortest_set = set(shortest_path)
    children = {}

    for cell in visited:
        children[cell] = []

    for child, par in parent.items():
        if par is not None:
            children[par].append(child)

    alternative_paths = []

    for cell in visited:
        if cell in shortest_set:
            continue

        # uç nokta mı? yani çocuğu yoksa alternatif dal olarak al
        if len(children.get(cell, [])) == 0:
            path = build_path(parent, cell)

            # kırmızı en kısa yolun aynısını alternatif diye çizme
            if len(path) > 2:
                alternative_paths.append(path)

    alternative_paths.sort(key=len, reverse=True)

    return alternative_paths[:8]


def solve_maze_bfs(matrix):
    start_time = time.time()

    rows = len(matrix)
    cols = len(matrix[0])

    start = (1, 1)
    end = (rows - 2, cols - 2)

    queue = deque([start])
    visited = set([start])

    parent = {}
    parent[start] = None

    # BFS tüm ulaşılabilir yolları gezer
    while queue:
        current = queue.popleft()

        for neighbor in get_open_neighbors(matrix, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    if end in parent:
        shortest_path = build_path(parent, end)
    else:
        shortest_path = []

    alternative_paths = build_alternative_paths(
        parent,
        visited,
        shortest_path
    )

    end_time = time.time()

    return {
        "path": shortest_path,
        "alternative_paths": alternative_paths,
        "visited_count": len(visited),
        "path_length": len(shortest_path),
        "solve_time": end_time - start_time,
        "algorithm": "BFS"
    }


def find_shortest_path(matrix):
    result = solve_maze_bfs(matrix)
    return result["path"]