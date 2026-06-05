import pygame
import time

from maze_generator import generate_maze
from solver import solve_maze_bfs
from renderer import draw_maze, draw_solution_path, draw_alternative_paths


pygame.init()

BG_COLOR = (18, 18, 18)
PANEL_COLOR = (35, 35, 35)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER = (100, 100, 100)
TEXT_COLOR = (235, 235, 235)
YELLOW = (255, 230, 0)

small_font = pygame.font.SysFont("Arial", 18)
title_font = pygame.font.SysFont("Arial", 32)

clock = pygame.time.Clock()

maze_size = 31
matrix = []
path = []
alternative_paths = []

visited_count = 0
path_length = 0
solve_time = 0
generation_time = 0

show_alternatives = False
show_solution = False

fullscreen = False

screen_width, screen_height = 1200, 800
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Maze Solver Project")


def get_screen_size():
    info = pygame.display.Info()
    return info.current_w, info.current_h


def calculate_layout():
    global panel_width, maze_area_width, maze_area_height
    global cell_size, maze_offset_x, maze_offset_y

    panel_width = max(430, screen_width // 4)
    maze_area_width = screen_width - panel_width
    maze_area_height = screen_height

    cell_size = min(
        maze_area_width // maze_size,
        maze_area_height // maze_size
    )

    maze_pixel_width = maze_size * cell_size
    maze_pixel_height = maze_size * cell_size

    maze_offset_x = (maze_area_width - maze_pixel_width) // 2

    label_space = 35
    maze_offset_y = (maze_area_height - maze_pixel_height + label_space) // 2


def create_new_maze(size):
    global maze_size, matrix, path, alternative_paths
    global visited_count, path_length, solve_time, generation_time
    global show_alternatives, show_solution

    maze_size = size

    start_generation = time.time()
    matrix, tree_parent = generate_maze(size, size)
    end_generation = time.time()

    generation_time = end_generation - start_generation

    result = solve_maze_bfs(matrix)

    path = result["path"]
    alternative_paths = result["alternative_paths"]
    visited_count = result["visited_count"]
    path_length = result["path_length"]
    solve_time = result["solve_time"]

    show_alternatives = False
    show_solution = False

    calculate_layout()


class Button:
    def __init__(self, text, x, y, w, h, action):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR

        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (165, 165, 165), self.rect, 2, border_radius=8)

        text_surface = small_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()


def toggle_alternatives():
    global show_alternatives
    show_alternatives = not show_alternatives


def toggle_solution():
    global show_solution
    show_solution = not show_solution


def show_all_paths():
    global show_alternatives, show_solution
    show_alternatives = True
    show_solution = True


def toggle_fullscreen():
    global fullscreen, screen, screen_width, screen_height

    fullscreen = not fullscreen

    if fullscreen:
        screen_width, screen_height = get_screen_size()
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    else:
        screen_width, screen_height = 1200, 800
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    calculate_layout()


def create_buttons():
    panel_x = maze_area_width
    button_x = panel_x + 30
    button_w = panel_width - 60
    button_h = 40
    gap = 10
    start_y = 110

    return [
        Button("New Maze", button_x, start_y, button_w, button_h, lambda: create_new_maze(maze_size)),
        Button("Show Alternative Paths", button_x, start_y + 1 * (button_h + gap), button_w, button_h, toggle_alternatives),
        Button("Show Shortest Path", button_x, start_y + 2 * (button_h + gap), button_w, button_h, toggle_solution),
        Button("Show All Paths", button_x, start_y + 3 * (button_h + gap), button_w, button_h, show_all_paths),
        Button("Size 21 x 21", button_x, start_y + 4 * (button_h + gap), button_w, button_h, lambda: create_new_maze(21)),
        Button("Size 31 x 31", button_x, start_y + 5 * (button_h + gap), button_w, button_h, lambda: create_new_maze(31)),
        Button("Size 41 x 41", button_x, start_y + 6 * (button_h + gap), button_w, button_h, lambda: create_new_maze(41)),
        Button("Fullscreen", button_x, start_y + 7 * (button_h + gap), button_w, button_h, toggle_fullscreen),
    ]


def draw_panel():
    panel_x = maze_area_width

    pygame.draw.rect(screen, PANEL_COLOR, (panel_x, 0, panel_width, screen_height))

    title = title_font.render("Maze Solver", True, YELLOW)
    screen.blit(title, (panel_x + 30, 35))

    buttons = create_buttons()

    for button in buttons:
        button.draw(screen)

    line_y = 535

    pygame.draw.line(
        screen,
        (120, 120, 120),
        (panel_x + 30, line_y),
        (panel_x + panel_width - 30, line_y),
        2
    )

    left_x = panel_x + 30
    right_x = panel_x + panel_width // 2 + 10
    info_y = line_y + 25

    left_lines = [
    "Maze Statistics",
    f"Algorithm: BFS",
    f"Maze Size: {maze_size} x {maze_size}",
    f"Shortest Path: {path_length}",
    f"Alternative Routes: {len(alternative_paths)}",
    f"Visited Nodes: {visited_count}",
    f"Generation: {generation_time:.5f} s",
    f"Solve: {solve_time:.5f} s"
]

    right_lines = [
        "Keyboard Shortcuts",
        "R: New Maze",
        "A: Alternatives",
        "SPACE: Shortest Path",
        "P: All Paths",
        "F: Fullscreen",
        "1-2-3: Size",
        "ESC: Exit"
    ]

    for i, line in enumerate(left_lines):
        color = YELLOW if i == 0 else TEXT_COLOR
        text = small_font.render(line, True, color)
        screen.blit(text, (left_x, info_y + i * 25))

    for i, line in enumerate(right_lines):
        color = YELLOW if i == 0 else TEXT_COLOR
        text = small_font.render(line, True, color)
        screen.blit(text, (right_x, info_y + i * 25))


calculate_layout()
create_new_maze(maze_size)

running = True

while running:
    buttons = create_buttons()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE and not fullscreen:
            screen_width = event.w
            screen_height = event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            calculate_layout()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_r:
                create_new_maze(maze_size)

            elif event.key == pygame.K_a:
                toggle_alternatives()

            elif event.key == pygame.K_SPACE:
                toggle_solution()

            elif event.key == pygame.K_p:
                show_all_paths()

            elif event.key == pygame.K_f:
                toggle_fullscreen()

            elif event.key == pygame.K_1:
                create_new_maze(21)

            elif event.key == pygame.K_2:
                create_new_maze(31)

            elif event.key == pygame.K_3:
                create_new_maze(41)

        for button in buttons:
            button.handle_event(event)

    screen.fill(BG_COLOR)

    draw_maze(screen, matrix, cell_size, maze_offset_x, maze_offset_y)

    if show_alternatives:
        draw_alternative_paths(
            screen,
            alternative_paths,
            cell_size,
            maze_offset_x,
            maze_offset_y
        )

    if show_solution:
        draw_solution_path(
            screen,
            path,
            cell_size,
            maze_offset_x,
            maze_offset_y
        )

    start_label = small_font.render("START", True, (0, 255, 0))
    end_label = small_font.render("END", True, (0, 80, 255))

    screen.blit(start_label, (maze_offset_x + cell_size, maze_offset_y + cell_size - 24))
    screen.blit(end_label, (maze_offset_x + (maze_size - 4) * cell_size, maze_offset_y + (maze_size - 2) * cell_size + 5))

    draw_panel()

    pygame.display.update()
    clock.tick(60)

pygame.quit()