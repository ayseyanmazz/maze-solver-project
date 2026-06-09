import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 80, 255)
VISITED_COLOR = (0, 180, 255)
CURRENT_COLOR = (255, 220, 0)
PATH_COLOR = (255, 0, 0)
TREE_COLOR = (170, 170, 170)
GOAL_FOUND_COLOR = (0, 255, 100) # Hedefe ulaşınca yanacak renk

def get_cell_rect(row, col, cell_size, offset_x, offset_y):
    return (
        offset_x + col * cell_size,
        offset_y + row * cell_size,
        cell_size,
        cell_size
    )

def get_cell_center(row, col, cell_size, offset_x, offset_y):
    x = offset_x + col * cell_size + cell_size // 2
    y = offset_y + row * cell_size + cell_size // 2
    return x, y

def draw_maze(screen, matrix, cell_size, offset_x, offset_y, path_found=False):
    rows = len(matrix)
    cols = len(matrix[0])

    for r in range(rows):
        for c in range(cols):
            color = WHITE
            if matrix[r][c] == 1:
                color = BLACK

            pygame.draw.rect(
                screen,
                color,
                get_cell_rect(r, c, cell_size, offset_x, offset_y)
            )

    # Başlangıç Noktası (Yeşil)
    pygame.draw.rect(
        screen,
        GREEN,
        get_cell_rect(1, 1, cell_size, offset_x, offset_y)
    )

    # Bitiş Noktası (Yol bulunduysa Açık Yeşil/GOAL_FOUND, bulunmadıysa Mavi)
    end_color = GOAL_FOUND_COLOR if path_found else BLUE
    pygame.draw.rect(
        screen,
        end_color,
        get_cell_rect(rows - 2, cols - 2, cell_size, offset_x, offset_y)
    )

def draw_visited(screen, visited, cell_size, offset_x, offset_y):
    for r, c in visited:
        pygame.draw.rect(
            screen,
            VISITED_COLOR,
            get_cell_rect(r, c, cell_size, offset_x, offset_y)
        )

def draw_parent_tree(screen, parent, cell_size, offset_x, offset_y):
    for child, par in parent.items():
        if par is None:
            continue

        x1, y1 = get_cell_center(child[0], child[1], cell_size, offset_x, offset_y)
        x2, y2 = get_cell_center(par[0], par[1], cell_size, offset_x, offset_y)

        pygame.draw.line(screen, TREE_COLOR, (x1, y1), (x2, y2), 1)

def draw_current_node(screen, current, cell_size, offset_x, offset_y):
    if current is None:
        return
    r, c = current
    pygame.draw.rect(
        screen,
        CURRENT_COLOR,
        get_cell_rect(r, c, cell_size, offset_x, offset_y)
    )

def draw_solution_path(screen, path, cell_size, offset_x, offset_y):
    if len(path) < 2:
        return

    points = []
    for r, c in path:
        points.append(get_cell_center(r, c, cell_size, offset_x, offset_y))

    pygame.draw.lines(
        screen,
        PATH_COLOR,
        False,
        points,
        max(4, cell_size // 4)
    )

def draw_labels(screen, font, maze_size, cell_size, offset_x, offset_y):
    start_label = font.render("START", True, GREEN)
    end_label = font.render("END", True, BLUE)

    screen.blit(start_label, (offset_x + cell_size, offset_y + cell_size - 24))
    screen.blit(end_label, (offset_x + (maze_size - 4) * cell_size, offset_y + (maze_size - 2) * cell_size + 5))