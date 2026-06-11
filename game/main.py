import pygame
import time

from maze_generator import generate_maze
from solver import solve_maze_bfs
from renderer import draw_maze, draw_solution_path, draw_search_cells


pygame.init()

BG_COLOR = (18, 18, 18)
PANEL_COLOR = (35, 35, 35)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER = (100, 100, 100)
TEXT_COLOR = (235, 235, 235)
MUTED_TEXT = (190, 190, 190)
YELLOW = (255, 230, 0)

small_font = pygame.font.SysFont("Arial", 18)
button_font = pygame.font.SysFont("Arial", 19)
title_font = pygame.font.SysFont("Arial", 32)

clock = pygame.time.Clock()

maze_size = 31
matrix = []
path = []
search_edges = []

visited_count = 0
path_length = 0
solve_time = 0.0
generation_time = 0.0

show_search = False
show_solution = False

search_animation_index = 0
solution_animation_index = 0
animation_speed = 2

fullscreen = False

screen_width, screen_height = 1250, 800
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Maze Solver Project")

panel_width = 420
maze_area_width = screen_width - panel_width
maze_area_height = screen_height
cell_size = 20
maze_offset_x = 0
maze_offset_y = 0


def get_screen_size():
    info = pygame.display.Info()
    return info.current_w, info.current_h


def calculate_layout():
    global panel_width, maze_area_width, maze_area_height
    global cell_size, maze_offset_x, maze_offset_y

    panel_width = max(440, screen_width // 3)
    maze_area_width = screen_width - panel_width
    maze_area_height = screen_height

    cell_size = max(
        8,
        min(
            maze_area_width // maze_size,
            maze_area_height // maze_size
        )
    )

    maze_pixel_width = maze_size * cell_size
    maze_pixel_height = maze_size * cell_size

    maze_offset_x = (maze_area_width - maze_pixel_width) // 2
    maze_offset_y = (maze_area_height - maze_pixel_height) // 2


def solve_current_maze():
    global path, search_edges
    global visited_count, path_length, solve_time

    result = solve_maze_bfs(matrix)

    path = result["path"]
    search_edges = result["search_edges"]
    visited_count = result["visited_count"]
    path_length = result["path_length"]
    solve_time = result["solve_time"]


def create_new_maze(size):
    global maze_size, matrix, generation_time
    global show_search, show_solution
    global search_animation_index, solution_animation_index

    maze_size = size

    start_generation = time.time()
    matrix, _tree_parent = generate_maze(size, size)
    generation_time = time.time() - start_generation

    solve_current_maze()

    show_search = False
    show_solution = False
    search_animation_index = 0
    solution_animation_index = 0

    calculate_layout()


class Button:
    def __init__(self, text, x, y, w, h, action):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR

        pygame.draw.rect(surface, color, self.rect, border_radius=9)
        pygame.draw.rect(surface, (165, 165, 165), self.rect, 2, border_radius=9)

        text_surface = button_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()


def show_search_animation():
    global show_search, show_solution
    global search_animation_index, solution_animation_index

    show_search = True
    show_solution = False
    search_animation_index = 0
    solution_animation_index = 0


def show_shortest_path():
    global show_search, show_solution
    global search_animation_index, solution_animation_index

    show_search = True
    show_solution = True
    search_animation_index = len(search_edges)
    solution_animation_index = 0


def increase_speed():
    global animation_speed
    animation_speed = min(10, animation_speed + 1)


def decrease_speed():
    global animation_speed
    animation_speed = max(1, animation_speed - 1)


def toggle_fullscreen():
    global fullscreen, screen, screen_width, screen_height

    fullscreen = not fullscreen

    if fullscreen:
        screen_width, screen_height = get_screen_size()
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    else:
        screen_width, screen_height = 1250, 800
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    calculate_layout()


def create_buttons():
    panel_x = maze_area_width
    button_x = panel_x + 30
    button_w = panel_width - 60
    button_h = 40
    gap = 11
    start_y = 105

    return [
        Button("New Maze", button_x, start_y, button_w, button_h, lambda: create_new_maze(maze_size)),
        Button("Show Search", button_x, start_y + 1 * (button_h + gap), button_w, button_h, show_search_animation),
        Button("Show Shortest Path", button_x, start_y + 2 * (button_h + gap), button_w, button_h, show_shortest_path),
        Button("Size 21 x 21", button_x, start_y + 3 * (button_h + gap), button_w, button_h, lambda: create_new_maze(21)),
        Button("Size 31 x 31", button_x, start_y + 4 * (button_h + gap), button_w, button_h, lambda: create_new_maze(31)),
        Button("Size 41 x 41", button_x, start_y + 5 * (button_h + gap), button_w, button_h, lambda: create_new_maze(41)),
        Button("Fullscreen", button_x, start_y + 6 * (button_h + gap), button_w, button_h, toggle_fullscreen),
    ]


def draw_panel():
    panel_x = maze_area_width

    pygame.draw.rect(screen, PANEL_COLOR, (panel_x, 0, panel_width, screen_height))

    title = title_font.render("Maze Solver", True, YELLOW)
    screen.blit(title, (panel_x + 30, 35))

    buttons = create_buttons()
    for button in buttons:
        button.draw(screen)

    line_y = 485
    pygame.draw.line(
        screen,
        (120, 120, 120),
        (panel_x + 30, line_y),
        (panel_x + panel_width - 30, line_y),
        2
    )

    left_x = panel_x + 30
    right_x = panel_x + panel_width // 2 + 15
    info_y = line_y + 25

    left_lines = [
        ("Maze Statistics", YELLOW),
        ("Algorithm: BFS", TEXT_COLOR),
        (f"Maze Size: {maze_size} x {maze_size}", TEXT_COLOR),
        (f"Path Length: {path_length}", TEXT_COLOR),
        (f"Visited Nodes: {visited_count}", TEXT_COLOR),
        (f"Generation: {generation_time:.5f} s", TEXT_COLOR),
        (f"Solve: {solve_time:.5f} s", TEXT_COLOR),
        (f"Speed: {animation_speed}", TEXT_COLOR),
    ]

    right_lines = [
        ("Keyboard Shortcuts", YELLOW),
        ("R: New Maze", MUTED_TEXT),
        ("S: Show Search", MUTED_TEXT),
        ("SPACE: Shortest Path", MUTED_TEXT),
        ("F: Fullscreen", MUTED_TEXT),
        ("1-2-3: Size", MUTED_TEXT),
        ("UP/DOWN: Speed", MUTED_TEXT),
        ("ESC: Exit", MUTED_TEXT),
    ]

    for i, (line, color) in enumerate(left_lines):
        text = small_font.render(line, True, color)
        screen.blit(text, (left_x, info_y + i * 24))

    for i, (line, color) in enumerate(right_lines):
        text = small_font.render(line, True, color)
        screen.blit(text, (right_x, info_y + i * 24))


def draw_labels():
    start_label = small_font.render("START", True, (0, 255, 0))
    end_label = small_font.render("END", True, (0, 80, 255))

    screen.blit(
        start_label,
        (
            maze_offset_x + cell_size,
            maze_offset_y + cell_size - 24
        )
    )

    screen.blit(
        end_label,
        (
            maze_offset_x + (maze_size - 5) * cell_size,
            maze_offset_y + (maze_size - 2) * cell_size + 5
        )
    )


calculate_layout()
create_new_maze(maze_size)

running = True

while running:
    buttons = create_buttons()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE and not fullscreen:
            screen_width = max(900, event.w)
            screen_height = max(650, event.h)
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            calculate_layout()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_r:
                create_new_maze(maze_size)

            elif event.key == pygame.K_s:
                show_search_animation()

            elif event.key == pygame.K_SPACE:
                show_shortest_path()

            elif event.key == pygame.K_f:
                toggle_fullscreen()

            elif event.key == pygame.K_1:
                create_new_maze(21)

            elif event.key == pygame.K_2:
                create_new_maze(31)

            elif event.key == pygame.K_3:
                create_new_maze(41)

            elif event.key == pygame.K_UP:
                increase_speed()

            elif event.key == pygame.K_DOWN:
                decrease_speed()

        for button in buttons:
            button.handle_event(event)

    screen.fill(BG_COLOR)

    draw_maze(screen, matrix, cell_size, maze_offset_x, maze_offset_y)

    if show_search:
        search_animation_index = min(
            len(search_edges),
            search_animation_index + animation_speed
        )

        draw_search_cells(
            screen,
            search_edges[:search_animation_index],
            cell_size,
            maze_offset_x,
            maze_offset_y
        )

    if show_solution:
        solution_animation_index = min(
            len(path),
            solution_animation_index + animation_speed
        )

        draw_solution_path(
            screen,
            path[:solution_animation_index],
            cell_size,
            maze_offset_x,
            maze_offset_y
        )

    draw_labels()
    draw_panel()

    pygame.display.update()
    clock.tick(60)

pygame.quit()