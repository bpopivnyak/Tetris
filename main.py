import pygame
import random

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 300#ширина екрану
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define shapes of tetrominoes
tetrominoes = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]]   # Z
]

# Define colors of tetrominoes
tetromino_colors = [
    (0, 255, 255),  # Cyan
    (128, 0, 128),  # Purple
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (0, 255, 0),    # Green
    (255, 255, 0),  # Yellow
    (255, 0, 0)     # Red
]

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Create the game clock
clock = pygame.time.Clock()

# Function to draw a tetromino on the screen
def draw_tetromino(tetromino, color, position):
    for y in range(len(tetromino)):
        for x in range(len(tetromino[y])):
            if tetromino[y][x]:
                pygame.draw.rect(screen, color, pygame.Rect((position[0] + x) * BLOCK_SIZE, (position[1] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Function to check if a tetromino is colliding with the board or another tetromino
def is_collision(board, tetromino, position):
    for y in range(len(tetromino)):
        for x in range(len(tetromino[y])):
            if tetromino[y][x] and (position[0] + x < 0 or position[0] + x >= BOARD_WIDTH or position[1] + y >= BOARD_HEIGHT or board[position[1] + y][position[0] + x]):
                return True
    return False

# Function to merge a tetromino with the board
def merge_with_board(board, tetromino, position):
    for y in range(len(tetromino)):
        for x in range(len(tetromino[y])):
            if tetromino[y][x]:
                board[position[1] + y][position[0] + x] = 1

# Function to remove completed rows from the board
def remove_completed_rows(board):
    completed_rows = 0
    for y in range(BOARD_HEIGHT):
        if all(board[y]):
            del board[y]
            board.insert(0, [0] * BOARD_WIDTH)
            completed_rows += 1
    return completed_rows

# Function to generate a new tetromino
def new_tetromino():
    return random.choice(tetrominoes), random.choice(tetromino_colors), [BOARD_WIDTH // 2 - 1, 0]

# Main game loop
def main():
    board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    tetromino, color, position = new_tetromino()
    game_over = False
    fall_time = 0
    fall_speed = 0.5

    while not game_over:
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Handle keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if not is_collision(board, tetromino, [position[0] - 1, position[1]]):
                position[0] -= 1
        if keys[pygame.K_RIGHT]:
            if not is_collision(board, tetromino, [position[0] + 1, position[1]]):
                position[0] += 1
        if keys[pygame.K_DOWN]:
            if not is_collision(board, tetromino, [position[0], position[1] + 1]):
                position[1] += 1

        # Move tetromino down at regular intervals
        fall_time += clock.get_rawtime()
        clock.tick()
        if fall_time / 1000 >= fall_speed:
            if not is_collision(board, tetromino, [position[0], position[1] + 1]):
                position[1] += 1
            else:
                merge_with_board(board, tetromino, position)
                completed_rows = remove_completed_rows(board)
                if completed_rows:
                    fall_speed = max(0.1, fall_speed - 0.03 * completed_rows)
                tetromino, color, position = new_tetromino()
                if is_collision(board, tetromino, position):
                    game_over = True
            fall_time = 0

        # Draw the board
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if board[y][x]:
                    pygame.draw.rect(screen, BLACK, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        # Draw the current tetromino
        draw_tetromino(tetromino, color, position)

        pygame.display.flip()

    pygame.quit()

def main_game():
    main()

