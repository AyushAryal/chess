import pygame
import os
import sys
import chess
from pygame_functions import *

previous_position = None


def handle_events(window, board):
    global previous_position
    partition = window.get_height() // 8
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            primary_mouse_button_pressed, *_ = pygame.mouse.get_pressed()
            if primary_mouse_button_pressed:
                y, x = pygame.mouse.get_pos()
                position = (x//partition, y//partition)

                x, y = position
                if board.board[x][y] and board.board[x][y].color == board.current_player:
                    previous_position = position
                    options = board.board[x][y].moves(board, (x, y))
                elif previous_position:
                    previous_x, previous_y = previous_position
                    options = board.board[previous_x][previous_y].moves(
                        board, (previous_x, previous_y))
                    if position in options:
                        board.make_move(previous_position, position, None)
                        board.switch_player()
                        previous_position = False


def render(window, board):
    global previous_position
    render_gui_board(window, board)
    if previous_position:
        x, y = previous_position
        options = board.board[x][y].moves(board, (x, y))
        render_options(window, options)


def render_options(window, options):
    partition = window.get_height() // 8
    option_icon = pygame.image.load(
        os.path.join("images", "possiblepostions1.png"))
    option_icon = pygame.transform.scale(option_icon, (partition, partition))
    for option_x, option_y in options:
        window.blit(option_icon, (option_y * partition, option_x * partition))
    return options


def render_gui_board(window, board):
    # Render chessboard
    chessboard = pygame.image.load(
        os.path.join("images", "chessboard.jpg"))
    chessboard = pygame.transform.scale(
        chessboard, (window.get_width(), window.get_height()))
    window.blit(chessboard, (0, 0))

    # Render peices
    partition = window.get_height() // 8
    for x, row in enumerate(board.board):
        for y, piece in enumerate(row):
            if piece:
                filename = (piece.color + piece.type + ".png").lower()
                piece_sprite = pygame.image.load(
                    os.path.join("Assets", filename))
                piece_sprite = pygame.transform.scale(
                    piece_sprite, (partition, partition))
                window.blit(piece_sprite, (y*partition, x*partition))


def main():
    pygame.init()
    height = 600
    width = 600
    window = pygame.display.set_mode((height, width))
    pygame.display.set_caption("PyChess")

    board = chess.Board()
    board.setup_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    while not board.is_checkmate():
        handle_events(window, board)
        render(window, board)
        pygame.display.update()

    board.switch_player()
    print(f'Game over. Winner is {board.current_player}')


if __name__ == '__main__':
    main()
