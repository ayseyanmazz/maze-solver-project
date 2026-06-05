from collections import deque

def find_shortest_path(matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    start = (1, 1)
    end = (num_rows - 2, num_cols - 2)

    queue = deque()
    queue.append((start, [start]))

    visited = set()
    visited.add(start)

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    while queue:
        (r, c), path = queue.popleft()

        if (r, c) == end:
            return path

        for dr, dc in directions:
            new_r = r + dr
            new_c = c + dc

            if 0 <= new_r < num_rows and 0 <= new_c < num_cols:
                if matrix[new_r][new_c] == 0 and (new_r, new_c) not in visited:
                    visited.add((new_r, new_c))
                    queue.append(((new_r, new_c), path + [(new_r, new_c)]))

    return []