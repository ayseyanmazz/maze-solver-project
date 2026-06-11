# pyright: reportArgumentType=false, reportGeneralTypeIssues=false

from collections import deque
import time


DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1)
]


def get_neighbors(matrix, cell):
    r, c = cell
    rows = len(matrix)
    cols = len(matrix[0])

    neighbors = []

    for dr, dc in DIRECTIONS:
        nr = r + dr
        nc = c + dc

        if 0 <= nr < rows and 0 <= nc < cols:
            if matrix[nr][nc] == 0:
                neighbors.append((nr, nc))

    return neighbors


def build_path(parent, end):
    path = []
    current = end

    while current is not None:
        path.append(current)
        current = parent.get(current)

    path.reverse()
    return path


def solve_maze_bfs(matrix):
    start_time = time.time()

    rows = len(matrix)
    cols = len(matrix[0])

    start = (1, 1)
    end = (rows - 2, cols - 2)

    queue = deque()
    queue.append(start)

    visited = set()
    visited.add(start)

    parent = {}
    parent[start] = None

    search_edges = []

    while queue:
        current = queue.popleft()

        if current == end:
            break

        for neighbor in get_neighbors(matrix, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                search_edges.append((current, neighbor))
                queue.append(neighbor)

    path = build_path(parent, end) if end in parent else []

    return {
        "algorithm": "BFS",
        "path": path,
        "search_edges": search_edges,
        "visited_count": len(visited),
        "path_length": len(path),
        "solve_time": time.time() - start_time
    }


def solve_maze_dfs(matrix):
    start_time = time.time()

    rows = len(matrix)
    cols = len(matrix[0])

    start = (1, 1)
    end = (rows - 2, cols - 2)

    stack = []
    stack.append(start)

    visited = set()
    visited.add(start)

    parent = {}
    parent[start] = None

    search_edges = []

    while stack:
        current = stack.pop()

        if current == end:
            break

        for neighbor in get_neighbors(matrix, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                search_edges.append((current, neighbor))
                stack.append(neighbor)

    path = build_path(parent, end) if end in parent else []

    return {
        "algorithm": "DFS",
        "path": path,
        "search_edges": search_edges,
        "visited_count": len(visited),
        "path_length": len(path),
        "solve_time": time.time() - start_time
    }


def solve_maze(matrix, algorithm):
    if algorithm == "DFS":
        return solve_maze_dfs(matrix)

    return solve_maze_bfs(matrix)


def find_shortest_path(matrix):
    result = solve_maze_bfs(matrix)
    return result["path"]