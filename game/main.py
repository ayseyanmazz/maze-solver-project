import pygame
import time

# Imported from previously translated modules
from maze_generator import generate_maze
from solver import find_shortest_path
from renderer import draw_maze, draw_solution_path

pygame.init()

CELL_SIZE = 25
OFFSET_Y = 40

font = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()

show_solution = False
animation_index = 0
animation_speed = 1


def create_new_maze(size):
    global matrix
    global path
    global solution_time
    global screen
    global num_rows
    global num_cols
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global show_solution
    global animation_index
    global tree_parent

    matrix, tree_parent = generate_maze(size, size)   
    start_time = time.time()
    path = find_shortest_path(matrix)
    end_time = time.time()

    solution_time = end_time - start_time

    num_rows = len(matrix)
    num_cols = len(matrix[0])

    SCREEN_WIDTH = num_cols * CELL_SIZE
    SCREEN_HEIGHT = num_rows * CELL_SIZE + OFFSET_Y

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Project")

    show_solution = False
    animation_index = 0


create_new_maze(31)

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                create_new_maze(31)

            elif event.key == pygame.K_SPACE:
                show_solution = not show_solution

                if show_solution:
                    animation_index = 0

            elif event.key == pygame.K_1:
                create_new_maze(21)

            elif event.key == pygame.K_2:
                create_new_maze(31)

            elif event.key == pygame.K_3:
                create_new_maze(41)

            elif event.key == pygame.K_UP:
                animation_speed += 1
                if animation_speed > 10:
                    animation_speed = 10

            elif event.key == pygame.K_DOWN:
                animation_speed -= 1
                if animation_speed < 1:
                    animation_speed = 1    
                

    screen.fill((0, 0, 0))

    draw_maze(screen, matrix, CELL_SIZE)

    if show_solution:
        # Step increment plus speed modifier
        animation_index += 1
        animation_index += animation_speed

        if animation_index > len(path):
            animation_index = len(path)

        draw_solution_path(
            screen,
            path[:animation_index],
            CELL_SIZE
        )

    # Info HUD text translated to English
    info_text = font.render(
        f"Path: {len(path)} | Time: {solution_time:.5f} s | Speed: {animation_speed} | R: New | SPACE: Solve | 1-2-3: Size",
        True,
        (255, 255, 0)
    )
    
    screen.blit(info_text, (10, 10))

    start_text = font.render("START", True, (0, 255, 0))
    end_text = font.render("END", True, (0, 0, 255))

    screen.blit(start_text, (5, OFFSET_Y + 5))

    screen.blit(
        end_text,
        (
            (num_cols - 4) * CELL_SIZE,
            (num_rows - 2) * CELL_SIZE + OFFSET_Y + 5
        )
    )

    pygame.display.update()
    clock.tick(60)

pygame.quit()