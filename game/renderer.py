import pygame

WHITE = (245, 245, 245)
BLACK = (0, 0, 0)
GREEN = (0, 220, 0)
END_BLUE = (0, 80, 255)
RED = (255, 0, 0)
SEARCH_BLUE = (0, 170, 255)


def get_cell_center(row, col, cell_size, offset_x, offset_y):
    x = offset_x + col * cell_size + cell_size // 2
    y = offset_y + row * cell_size + cell_size // 2
    return x, y


def draw_maze(screen, matrix, cell_size, offset_x, offset_y):
    rows = len(matrix)
    cols = len(matrix[0])

    for r in range(rows):
        for c in range(cols):
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
        END_BLUE,
        (
            offset_x + (cols - 2) * cell_size,
            offset_y + (rows - 2) * cell_size,
            cell_size,
            cell_size
        )
    )


def draw_search_cells(screen, search_edges, cell_size, offset_x, offset_y):
    visited_cells = set()

    for start_cell, end_cell in search_edges:
        visited_cells.add(start_cell)
        visited_cells.add(end_cell)

    for r, c in visited_cells:
        pygame.draw.rect(
            screen,
            SEARCH_BLUE,
            (
                offset_x + c * cell_size,
                offset_y + r * cell_size,
                cell_size,
                cell_size
            )
        )


def draw_solution_path(screen, path, cell_size, offset_x, offset_y):
    points = []

    for r, c in path:
        points.append(get_cell_center(r, c, cell_size, offset_x, offset_y))

    if len(points) > 1:
        pygame.draw.lines(
            screen,
            RED,
            False,
            points,
            max(4, cell_size // 4)
        )