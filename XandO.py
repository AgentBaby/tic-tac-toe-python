import pygame as pg
import sys
import time
from pygame.locals import QUIT, MOUSEBUTTONDOWN

# ---------- settings ----------
WIDTH = 400
HEIGHT = 400
STATUS_HEIGHT = 100
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (10, 10, 10)
X_COLOR = (220, 50, 50)
O_COLOR = (40, 90, 220)
WIN_LINE_COLOR = (0, 160, 70)

CELL = WIDTH // 3

# ---------- game state ----------
current_player = 'x'
winner = None
draw = False
board = [[None] * 3 for _ in range(3)]

# ---------- pygame setup ----------
pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT + STATUS_HEIGHT))
pg.display.set_caption("Tic Tac Toe")


def show_opening():
    """Title screen drawn in code (no image needed)."""
    screen.fill((20, 20, 40))
    title_font = pg.font.Font(None, 72)
    sub_font = pg.font.Font(None, 30)

    title = title_font.render("Tic Tac Toe", True, WHITE)
    sub = sub_font.render("X goes first. Click a square to play.", True, (200, 200, 220))

    screen.blit(title, title.get_rect(center=(WIDTH // 2, (HEIGHT + STATUS_HEIGHT) // 2 - 20)))
    screen.blit(sub, sub.get_rect(center=(WIDTH // 2, (HEIGHT + STATUS_HEIGHT) // 2 + 35)))
    pg.display.update()
    time.sleep(1.5)


def draw_board():
    screen.fill(WHITE)
    # vertical lines
    pg.draw.line(screen, LINE_COLOR, (CELL, 0), (CELL, HEIGHT), 7)
    pg.draw.line(screen, LINE_COLOR, (CELL * 2, 0), (CELL * 2, HEIGHT), 7)
    # horizontal lines
    pg.draw.line(screen, LINE_COLOR, (0, CELL), (WIDTH, CELL), 7)
    pg.draw.line(screen, LINE_COLOR, (0, CELL * 2), (WIDTH, CELL * 2), 7)
    draw_status()


def draw_status():
    if draw:
        message = "Game Draw!"
    elif winner is None:
        message = current_player.upper() + "'s Turn"
    else:
        message = winner.upper() + " won!"

    font = pg.font.Font(None, 30)
    text = font.render(message, True, WHITE)

    screen.fill(BLACK, (0, HEIGHT, WIDTH, STATUS_HEIGHT))
    screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT + STATUS_HEIGHT // 2)))
    pg.display.update()


def draw_x(row, col):
    margin = 25
    left = col * CELL + margin
    right = (col + 1) * CELL - margin
    top = row * CELL + margin
    bottom = (row + 1) * CELL - margin
    pg.draw.line(screen, X_COLOR, (left, top), (right, bottom), 10)
    pg.draw.line(screen, X_COLOR, (right, top), (left, bottom), 10)


def draw_o(row, col):
    center = (col * CELL + CELL // 2, row * CELL + CELL // 2)
    pg.draw.circle(screen, O_COLOR, center, CELL // 2 - 25, 10)


def place_mark(row, col):
    global current_player
    board[row][col] = current_player
    if current_player == 'x':
        draw_x(row, col)
        current_player = 'o'
    else:
        draw_o(row, col)
        current_player = 'x'
    pg.display.update()


def cell_center(row, col):
    return (col * CELL + CELL // 2, row * CELL + CELL // 2)


def check_win():
    global winner, draw

    # rows
    for row in range(3):
        if board[row][0] is not None and board[row][0] == board[row][1] == board[row][2]:
            winner = board[row][0]
            pg.draw.line(screen, WIN_LINE_COLOR, cell_center(row, 0), cell_center(row, 2), 6)
            break

    # columns
    if winner is None:
        for col in range(3):
            if board[0][col] is not None and board[0][col] == board[1][col] == board[2][col]:
                winner = board[0][col]
                pg.draw.line(screen, WIN_LINE_COLOR, cell_center(0, col), cell_center(2, col), 6)
                break

    # diagonals
    if winner is None and board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
        winner = board[0][0]
        pg.draw.line(screen, WIN_LINE_COLOR, cell_center(0, 0), cell_center(2, 2), 6)

    if winner is None and board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
        winner = board[0][2]
        pg.draw.line(screen, WIN_LINE_COLOR, cell_center(0, 2), cell_center(2, 0), 6)

    # draw (board full, no winner)
    if winner is None and all(all(cell for cell in row) for row in board):
        draw = True

    draw_status()


def handle_click():
    x, y = pg.mouse.get_pos()

    # ignore clicks on the status bar
    if y >= HEIGHT:
        return

    col = x // CELL
    row = y // CELL

    if board[row][col] is None:
        place_mark(row, col)
        check_win()


def reset_game():
    global board, winner, draw, current_player
    time.sleep(3)
    board = [[None] * 3 for _ in range(3)]
    winner = None
    draw = False
    current_player = 'x'
    draw_board()


# ---------- start ----------
show_opening()
draw_board()

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            handle_click()
            if winner or draw:
                reset_game()

    pg.display.update()
    clock.tick(FPS)
