import pygame

OFFSET_Y = 40

def draw_maze(screen, matrix, cell_size):

    num_rows = len(matrix)
    num_cols = len(matrix[0])

    for r in range(num_rows):
        for c in range(num_cols):

            if matrix[r][c] == 1:
                color = (0, 0, 0)
            else:
                color = (255, 255, 255)

            pygame.draw.rect(
                screen,
                color,
                (
                    c * cell_size,
                    r * cell_size + OFFSET_Y,
                    cell_size,
                    cell_size
                )
            )

    # Draw the start cell (Green)
    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (
            1 * cell_size,
            1 * cell_size + OFFSET_Y,
            cell_size,
            cell_size
        )
    )

    # Draw the end cell (Blue)
    pygame.draw.rect(
        screen,
        (0, 0, 255),
        (
            (num_cols - 2) * cell_size,
            (num_rows - 2) * cell_size + OFFSET_Y,
            cell_size,
            cell_size
        )
    )


def draw_solution_path(screen, path, cell_size):

    points = []

    for r, c in path:

        x = c * cell_size + cell_size // 2
        y = r * cell_size + cell_size // 2 + OFFSET_Y

        points.append((x, y))

    if len(points) > 1:
        pygame.draw.lines(
            screen,
            (255, 0, 0),
            False,
            points,
            5
        )