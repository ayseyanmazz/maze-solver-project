import random

def generate_maze(rows=31, cols=31):
    matrix = [[1 for _ in range(cols)] for _ in range(rows)]

    start = (1, 1)
    matrix[1][1] = 0

    stack = [start]
    visited = {start}

    # TREE structure: child -> parent
    parent = {
        start: None
    }

    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    while stack:
        r, c = stack[-1]

        neighbors = []

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            if 1 <= nr < rows - 1 and 1 <= nc < cols - 1:
                if (nr, nc) not in visited:
                    neighbors.append((nr, nc, dr, dc))

        if neighbors:
            nr, nc, dr, dc = random.choice(neighbors)

            # Break the wall
            matrix[r + dr // 2][c + dc // 2] = 0
            matrix[nr][nc] = 0

            visited.add((nr, nc))
            stack.append((nr, nc))

            # TREE connection
            parent[(nr, nc)] = (r, c)

        else:
            stack.pop()

    return matrix, parent