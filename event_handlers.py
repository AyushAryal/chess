import pygame
import sys
import ai
import os
from button import Button

previous_position = None

def promote_sub_screen(window, board):
    start_screen_bg = pygame.image.load(
        os.path.join("Assets", "start_screen.jpg"))
    start_screen_bg = pygame.transform.scale(
        start_screen_bg, (window.get_width(), window.get_height()))
    font = pygame.font.SysFont("FiraCode", 40)
    bg_color = pygame.Color(219, 56, 44, 255)
    
    queen = Button(pygame.Rect(250, 200, 300, 60), "Queen", font=font, bg_color=bg_color,
                            text_color=pygame.Color(255, 255, 255), callback=lambda: "q")
    rook = Button(pygame.Rect(250, 300, 300, 60), "Rook", font=font, bg_color=bg_color,
                            text_color=pygame.Color(255, 255, 255), callback=lambda: "r")
    bishop = Button(pygame.Rect(250, 400, 300, 60), "Bishop", font=font, bg_color=bg_color,
                            text_color=pygame.Color(255, 255, 255), callback=lambda: "b")
    knight = Button(pygame.Rect(250, 500, 300, 60), "Knight", font=font, bg_color=bg_color,
                            text_color=pygame.Color(255, 255, 255), callback=lambda: "n")

    buttons = (queen, rook, bishop, knight)

    while True:
        window.blit(start_screen_bg, (0, 0))
        for button in buttons:
            button.draw(window)
        if promotion_piece:= handle_event_button_screen(window, buttons):
            return promotion_piece
        pygame.display.update()
        
def handle_gameplay_events(window, board, ai_enabled):
    global previous_position
    partition = window.get_height() // board.size
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
                        move_x, _ = position
                        promotion_piece = None
                        if board.board[previous_x][previous_y].type == 'p' and (move_x == 0 or move_x == board.size - 1):
                            promotion_piece = promote_sub_screen(window, board)
                        board.make_move(previous_position, position, promotion_piece)
                        board.switch_player()
                        if ai_enabled and not board.cannot_move():
                            board.make_move(*ai.get_best_move(board))
                            board.switch_player()
                        previous_position = False

def handle_event_button_screen(window, buttons):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            primary_mouse_button_pressed, *_ = pygame.mouse.get_pressed()
            if primary_mouse_button_pressed:
                mouse_position = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(mouse_position):
                        return button.callback()

def handle_event_fen_screen(window, buttons, text_input):
    events = pygame.event.get()
    text_input.update(events)
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            primary_mouse_button_pressed, *_ = pygame.mouse.get_pressed()
            if primary_mouse_button_pressed:
                mouse_position = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(mouse_position):
                        return button.callback(text_input.get_text())

