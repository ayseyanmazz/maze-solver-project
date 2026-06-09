import pygame
from maze_generator import generate_maze  # Dosya ismini maze_generator yapmayı unutmayın!
from solver import BFSVisualizer
from renderer import (
    draw_maze,
    draw_visited,
    draw_parent_tree,
    draw_current_node,
    draw_solution_path,
    draw_labels
)

pygame.init()

WIDTH = 1400
HEIGHT = 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Algorithm Visualizer")
clock = pygame.time.Clock()

BG = (18, 18, 18)
PANEL = (35, 35, 35)
WHITE = (240, 240, 240)
YELLOW = (255, 220, 0)

font = pygame.font.SysFont("Arial", 20)
title_font = pygame.font.SysFont("Arial", 30)

maze_size = 31
matrix = generate_maze(maze_size, maze_size)
visualizer = BFSVisualizer(matrix)

panel_width = 350
maze_area_width = WIDTH - panel_width
cell_size = min(maze_area_width // maze_size, HEIGHT // maze_size)

maze_offset_x = (maze_area_width - maze_size * cell_size) // 2
maze_offset_y = (HEIGHT - maze_size * cell_size) // 2

running_bfs = False
paused = False

class Button:
    def __init__(self, text, x, y, w, h, action):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action

    def draw(self):
        mouse = pygame.mouse.get_pos()
        color = (90, 90, 90) if self.rect.collidepoint(mouse) else (65, 65, 65)
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        txt = font.render(self.text, True, WHITE)
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

def create_new_maze():
    global matrix, visualizer, running_bfs
    matrix = generate_maze(maze_size, maze_size)
    visualizer = BFSVisualizer(matrix)
    running_bfs = False

def start_bfs():
    global running_bfs
    running_bfs = True

def pause_bfs():
    global paused
    paused = not paused

def reset_bfs():
    global visualizer, running_bfs
    visualizer.reset()
    running_bfs = False

buttons = [
    Button("Generate Maze", 1080, 120, 250, 45, create_new_maze),
    Button("Start BFS", 1080, 180, 250, 45, start_bfs),
    Button("Pause", 1080, 240, 250, 45, pause_bfs),
    Button("Reset", 1080, 300, 250, 45, reset_bfs)
]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        for button in buttons:
            button.click(event)

    if running_bfs:
        if not paused:
            for _ in range(3):
                visualizer.step()
            visualizer.update_path_animation()

    screen.fill(BG)

    # Değişiklik: path_found durumunu draw_maze fonksiyonuna gönderiyoruz
    draw_maze(
        screen,
        matrix,
        cell_size,
        maze_offset_x,
        maze_offset_y,
        path_found=visualizer.path_found
    )

    draw_parent_tree(screen, visualizer.parent, cell_size, maze_offset_x, maze_offset_y)
    draw_visited(screen, visualizer.visited, cell_size, maze_offset_x, maze_offset_y)
    
    # Yol bulunduktan sonra mevcut arama imlecini gizleyebilirsiniz, temiz görünür
    if not visualizer.path_found:
        draw_current_node(screen, visualizer.current, cell_size, maze_offset_x, maze_offset_y)

    draw_solution_path(screen, visualizer.get_visible_path(), cell_size, maze_offset_x, maze_offset_y)
    draw_labels(screen, font, maze_size, cell_size, maze_offset_x, maze_offset_y)

    # Sağ Panel Çizimi
    pygame.draw.rect(screen, PANEL, (WIDTH - panel_width, 0, panel_width, HEIGHT))
    title = title_font.render("BFS VISUALIZER", True, YELLOW)
    screen.blit(title, (1060, 40))

    for button in buttons:
        button.draw()

    info = [
        f"Queue Size : {visualizer.get_queue_size()}",
        f"Visited : {visualizer.get_visited_count()}",
        f"Path Length : {visualizer.get_path_length()}",
        f"Current : {visualizer.current}",
        "",
        f"Finished : {visualizer.finished}",
        f"Found : {visualizer.path_found}"
    ]

    y = 420
    for line in info:
        txt = font.render(line, True, WHITE)
        screen.blit(txt, (1060, y))
        y += 35

    pygame.display.flip()
    clock.tick(60)