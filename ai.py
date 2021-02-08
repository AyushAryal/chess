from stockfish import Stockfish

def get_best_move(board):
    stockfish = Stockfish()
    move_list = []

    for move in board.moves:
        move_list.append(move.to_long_algebraic())

    stockfish.set_position(move_list)
    return long_algebraic_to_coordinate(stockfish.get_best_move())

def long_algebraic_to_coordinate(move):
    initial, final, promotion_piece = move[:2], move[2:4], move[4:]
    i_x, i_y = initial[1], initial[0]
    f_x, f_y = final[1], final[0]
    i_y = ord(i_y) - ord("a")
    f_y = ord(f_y) - ord("a")
    
    i_x = 8 - int(i_x)
    f_x = 8 - int(f_x)
    return ((i_x, i_y), (f_x, f_y), promotion_piece)    
    