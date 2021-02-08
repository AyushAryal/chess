import pygame
import os
import event_handlers
import chess
from button import Button
import pygame_textinput
import utils


def start_screen(window):
    start_screen_bg = pygame.image.load(
        os.path.join("Assets", "start_screen.jpg"))
    start_screen_bg = pygame.transform.scale(
        start_screen_bg, (window.get_width(), window.get_height()))
    font = pygame.font.SysFont("FiraCode", 40)
    bg_color = pygame.Color(219, 56, 44, 255)

    classic_button = Button(pygame.Rect(250, 200, 300, 60), "Classic", font=font, bg_color=bg_color,
                            text_color=pygame.Color(255, 255, 255), callback=lambda: game_screen)

    computer_button = Button(pygame.Rect(250, 300, 300, 60), "Computer", font=font, bg_color=bg_color,
                             text_color=pygame.Color(255, 255, 255), callback=lambda: (lambda win: game_screen(win, ai_enabled=True)))

    fen_button = Button(pygame.Rect(250, 400, 300, 60), "Setup Fen", font=font, bg_color=bg_color,
                        text_color=pygame.Color(255, 255, 255), callback=lambda: fen_screen)

    quit_button = Button(pygame.Rect(250, 500, 300, 60), "Quit", font=font, bg_color=bg_color,
                         text_color=pygame.Color(255, 255, 255), callback=lambda: True)

    buttons = (classic_button, computer_button, fen_button, quit_button)

    while not (new_screen := event_handlers.handle_event_button_screen(window, buttons)):
        window.blit(start_screen_bg, (0, 0))
        for button in buttons:
            button.draw(window)
        pygame.display.update()

    return new_screen


def render(window, board):
    render_gui_board(window, board)
    if event_handlers.previous_position:
        x, y = event_handlers.previous_position
        options = board.board[x][y].moves(board, (x, y))
        render_options(window, options)


def render_options(window, options):
    partition = window.get_height() // 8
    option_icon = pygame.image.load(
        os.path.join("Assets", "possible_positions.png"))
    option_icon = pygame.transform.scale(option_icon, (partition, partition))
    for option_x, option_y in options:
        window.blit(option_icon, (option_y * partition, option_x * partition))
    return options

def render_highlights(window, board):
    width = window.get_width() // board.size
    height = window.get_height() // board.size
    # Highlight selected piece
    if event_handlers.previous_position:
        x,y = event_handlers.previous_position
        utils.draw_rect_alpha(window, pygame.Color(0,255,0,50), (height*y, width*x, width, height))

    # Hightlight last move
    if board.moves:
        _, initial, final = board.moves[-1].moved_pieces[0]
        x, y = initial
        utils.draw_rect_alpha(window, pygame.Color(150,150,0,50), (height*y, width*x, width, height))
        x, y = final
        utils.draw_rect_alpha(window, pygame.Color(150,150,0,50), (height*y, width*x, width, height))
    
    # Highlight king if in check
    king = None
    if board.is_check(player="W"):
        king = board.find_piece("k", "W")
    elif board.is_check(player="B"):
        king = board.find_piece("k","B")
    if king:
        x, y = king
        utils.draw_rect_alpha(window, pygame.Color(255,64,64,255), (height*y, width*x, width, height))
    
    





def render_gui_board(window, board):
    # Render chessboard
    chessboard = pygame.image.load(
        os.path.join("Assets", "chessboard.jpg"))
    chessboard = pygame.transform.scale(
        chessboard, (window.get_width(), window.get_height()))
    window.blit(chessboard, (0, 0))

    # Render highlights
    render_highlights(window, board)

    # Render peices
    partition = window.get_height() // board.size
    for x, row in enumerate(board.board):
        for y, piece in enumerate(row):
            if piece:
                filename = (piece.color + piece.type + ".png").lower()
                piece_sprite = pygame.image.load(
                    os.path.join("Assets", filename))
                piece_sprite = pygame.transform.scale(
                    piece_sprite, (partition, partition))
                window.blit(piece_sprite, (y*partition, x*partition))


def game_screen(window, fen_position="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", ai_enabled=False):
    board = chess.Board()
    board.setup_fen(fen_position)

    while not board.cannot_move():
        event_handlers.handle_gameplay_events(window, board, ai_enabled)
        render(window, board)
        pygame.display.update()

    message = None
    if board.is_checkmate(player="B"):
        message = "White won. Play again?"
    elif board.is_checkmate(player="W"):
        message = "Black won. Play again?"
    else:
        message = "The game is a draw."

    return lambda win: gameover_screen(win, message)


def fen_screen(window):
    start_screen_bg = pygame.image.load(
        os.path.join("Assets", "start_screen.jpg"))
    start_screen_bg = pygame.transform.scale(
        start_screen_bg, (window.get_width(), window.get_height()))
    font = pygame.font.SysFont("FiraCode", 40)
    bg_color = pygame.Color(219, 56, 44, 255)

    start_game_button = Button(pygame.Rect(250, 500, 300, 50), "Start Game", font=font, bg_color=bg_color,
                               text_color=pygame.Color(255, 255, 255), callback=lambda p: (lambda win: game_screen(win, p)))
    back_button = Button(pygame.Rect(250, 600, 300, 50), "Go Back", font=font, bg_color=bg_color,
                         text_color=pygame.Color(255, 255, 255), callback=lambda _: start_screen)

    text_input = pygame_textinput.TextInput(
        initial_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", text_color=pygame.Color(255, 255, 255),
        font_family="FiraCode", font_size=22,
        cursor_color=pygame.Color(255, 255, 255))

    buttons = (start_game_button, back_button)

    while not (new_screen := event_handlers.handle_event_fen_screen(window, buttons, text_input)):
        window.blit(start_screen_bg, (0, 0))
        Button.draw_rect_alpha(window, pygame.Color(
            100, 56, 255, 100), pygame.Rect(10, 300, 780, 30))
        window.blit(text_input.get_surface(), (10, 300))
        start_game_button.draw(window)
        back_button.draw(window)
        pygame.display.update()

    return new_screen


def gameover_screen(window, message):
    start_screen_bg = pygame.image.load(
        os.path.join("Assets", "start_screen.jpg"))
    start_screen_bg = pygame.transform.scale(
        start_screen_bg, (window.get_width(), window.get_height()))
    font = pygame.font.SysFont("FiraCode", 40)
    bg_color = pygame.Color(219, 56, 44, 255)

    # Using a button with empty callback to act as a label
    gameover_label = Button(pygame.Rect(100, 300, 600, 100),
                            message, font=font, bg_color=bg_color)
    while True:
        window.blit(start_screen_bg, (0, 0))
        gameover_label.draw(window)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                primary_mouse_button_pressed, *_ = pygame.mouse.get_pressed()
                if primary_mouse_button_pressed:
                    return start_screen
