import pygame
import os
import chess

pygame.init()

height = 600
width = 600
win = pygame.display.set_mode((height, width))
partition = int(height/8)
pygame.display.set_caption("PyChess")

running = True
board = chess.Board()
board.setup_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")


def select_piece():
    ok=True
    while ok:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ok = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    initial_position=(int(pos[1]//partition)),(int(pos[1]//partition))
                    print(f"init:{initial_position}")
                    ok=False
    pygame.display.update()
    return(initial_position)

def get_options(board,initial):
    x,y=initial
    options = list(board.board[x][y].moves(board, (x, y)))
    print(options)
    circle=pygame.image.load(os.path.join("images","possiblepostions.jpg"))
    for option in options:
        win.blit(circle,(option[1]*partition,option[0]*partition))
        pygame.display.update()
    return options


def place_piece(options):
    ok=True
    while ok:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ok = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    initial_position=(int(pos[1]//partition)),(int(pos[1]//partition))
                    print(f"final:{initial_position}")
                    ok=False
    pygame.display.update()
    return(initial_position)


    


while running:
    chessboard=pygame.image.load(os.path.join("images","chessboard2.jpg"))
    win.blit(chessboard,(0,0))
    pygame.display.update()
    while not board.is_checkmate():
        initial=select_piece()
        options=get_options(board,initial)
        final=place_piece(options)

        board.make_move(initial,final,None)
        board.switch_player()
        board.print_board()

    pygame.display.update()
