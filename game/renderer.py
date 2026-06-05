import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 80, 255)
RED = (255, 0, 0)

ALTERNATIVE_COLORS = [
    (255, 220, 0),    # yellow
    (0, 220, 80),     # green
    (170, 80, 255),   # purple
    (255, 140, 0),    # orange
    (0, 200, 255),    # cyan
    (255, 80, 180)    # pink
]


def get_cell_center(row, col, cell_size, offset_x, offset_y):
    x = offset_x + col * cell_size + cell_size // 2
    y = offset_y + row * cell_size + cell_size // 2
    return x, y


def draw_maze(screen, matrix, cell_size, offset_x, offset_y):
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    for r in range(num_rows):
        for c in range(num_cols):
            color = BLACK if matrix[r][c] == 1 else WHITE

            pygame.draw.rect(
                screen,
                color,
                (
                    offset_x + c * cell_size,
                    offset_y + r * cell_size,
                    cell_size,
                    cell_size
                )
            )

    pygame.draw.rect(
        screen,
        GREEN,
        (
            offset_x + cell_size,
            offset_y + cell_size,
            cell_size,
            cell_size
        )
    )

    pygame.draw.rect(
        screen,
        BLUE,
        (
            offset_x + (num_cols - 2) * cell_size,
            offset_y + (num_rows - 2) * cell_size,
            cell_size,
            cell_size
        )
    )


def draw_path(screen, path, cell_size, offset_x, offset_y, color, width):
    points = []

    for r, c in path:
        points.append(get_cell_center(r, c, cell_size, offset_x, offset_y))

    if len(points) > 1:
        pygame.draw.lines(screen, color, False, points, width)


def draw_alternative_paths(screen, alternative_paths, cell_size, offset_x, offset_y):
    width = max(2, cell_size // 6)

    for index, path in enumerate(alternative_paths):
        color = ALTERNATIVE_COLORS[index % len(ALTERNATIVE_COLORS)]
        draw_path(screen, path, cell_size, offset_x, offset_y, color, width)


def draw_solution_path(screen, path, cell_size, offset_x, offset_y):
    width = max(4, cell_size // 4)
    draw_path(screen, path, cell_size, offset_x, offset_y, RED, width)