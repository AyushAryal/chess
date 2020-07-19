from piece import Piece
from itertools import groupby
from move import Move

class Board(object):
    def __init__(self, size=8):
        self.board = [[None]*size for _ in range(size)]
        self.size = size
        self.castling = {
            "W": {"k": False, "q": False},
            "B": {"k": False, "q": False},
        }
        self.enpassant = None
        self.moves = []

    def within_boundaries(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def setup_fen(self, position_fen):
        position, turn, castling, enpassant, _, _ = position_fen.split(" ")

        if enpassant != "-":
            y,x = list(enpassant.lower())
            y = ord(y) - ord('a')
            x = self.size - int(x)
            self.enpassant = (x,y)

        for char in castling:
            if char == "K":
                self.castling["W"]["k"] = True
            elif char == "Q":
                self.castling["W"]["q"] = True
            elif char == "k":
                self.castling["B"]["k"] = True
            elif char == "q":
                self.castling["B"]["q"] = True

        self.current_player = turn.upper()
        for y, row in enumerate(position.split("/")):
            grouped_alpha = ["".join(items) for _, items in groupby(
                row, lambda x: str.isdigit(x))]
            group = []
            for item in grouped_alpha:
                if item.isdigit():
                    group.append(item)
                else:
                    group.extend(list(item))
            x = 0
            for item in group:
                if item.isdigit():
                    x += int(item)
                elif item.isalpha():
                    if item.islower():
                        self.board[y][x] = Piece(item, "B")
                    else:
                        self.board[y][x] = Piece(item.lower(), "W")
                    x += 1

    def get_pieces(self, player=None):
        if not player:
            player = self.current_player
        player_pieces = []

        for x, row in enumerate(self.board):
            for y, piece in enumerate(row):
                if piece:
                    if piece.color == player:
                        player_pieces.append((x, y))
        return player_pieces

    def get_pinned_piece_positions(self, player=None):
        if not player:
            player = self.current_player

        player_pieces = self.get_pieces(player)
        opponent_pieces = self.get_pieces("W" if player == "B" else "B")

        king_position = board.find_piece("k", player)
        check_count = 0
        for opponent_position in opponent_pieces:
            for move_x, move_y in Piece.path(self, opponent_position):
                if (move_x, move_y) == king_position:
                    check_count += 1

        pinned_pieces = set()
        for x, y in player_pieces:
            if self.board[x][y].type == "k":
                continue
            removed_piece = self.board[x][y]
            self.board[x][y] = None
            check_count_next = 0
            for opponent_position in opponent_pieces:
                for move_x, move_y in Piece.path(self, opponent_position):
                    if (move_x, move_y) == king_position:
                        check_count_next += 1
            if check_count_next > check_count:
                pinned_pieces.add((x, y))
            self.board[x][y] = removed_piece
        return pinned_pieces

    def print_board(self):
        for row in self.board:
            fmt = ""
            for piece in row:
                if piece:
                    fmt += f" {str(piece)} "
                else:
                    fmt += " . "
            print(fmt)

    def switch_player(self):
        self.current_player = "W" if self.current_player == "B" else "B"

    def input_move(self):
        x, y = None, None
        while True:
            input_position = input(
                f"{self.current_player}:Select piece to move (example: 1,2): ")
            x, y = map(int, input_position.split(","))
            if self.board[x][y] and self.board[x][y].color == self.current_player:
                break
            else:
                print("Not a valid piece to move.")

        print(f"{self.board[x][y].type} selected")

        options = list(self.board[x][y].moves(self, (x, y)))
        print(f"your options are: {options}")

        x2, y2 = None, None
        while True:
            to = input(
                f"{self.current_player}:choose from list where you want to place it:")
            if int(to) >= 1 and int(to) <= len(options):
                x2, y2 = options[int(to)-1]
                break
            else:
                print("Not a valid option")

        promotion_piece = None
        if self.board[x][y].type == "p" and (x2 == 0 or x2 == self.size - 1):
            while True:
                choices = ("q", "r", "b", "n")
                promotion_piece = input("Enter which piece to promote to:")
                if promotion_piece in choices:
                    break
                else:
                    print("Enter correct promotion piece.")
        return ((x, y), (x2, y2), promotion_piece)

    def undo_move(self):
        move = self.moves.pop()
        for player, rights in move.delta_castling.items():
            for side, right in rights.items():
                self.castling[player][side] = not right
        self.enpassant = move.delta_enpassant_square

        for piece, (x, y), (x2, y2) in move.moved_pieces:
            if move.promotion_piece:
                self.board[x][y] = self.board[x2][y2]
                self.board[x][y].type = "p"
                self.board[x2][y2] = None
            else:
                self.board[x][y] = self.board[x2][y2]
                self.board[x2][y2] = None

        for piece, (x, y) in move.captured_pieces:
            self.board[x][y] = piece

    def make_move(self, initial_position, final_position, promotion_piece):
        move = Move()
        x, y = initial_position
        x2, y2 = final_position
        move.moved_pieces.append([self.board[x][y], (x, y), (x2, y2)])

        if self.board[x][y].type == "k":
            if (self.castling[self.board[x][y].color]["k"]):
                move.delta_castling[self.board[x][y].color]["k"] = False
            if self.castling[self.board[x][y].color]["q"]:
                move.delta_castling[self.board[x][y].color]["q"] = False
            self.castling[self.board[x][y].color]["k"] = False
            self.castling[self.board[x][y].color]["q"] = False
        if self.board[x][y].type == 'r':
            rook_initial_positions = {
                "W": {
                    "q": (self.size - 1, 0),
                    "k": (self.size-1, self.size-1)
                },
                "B": {
                    "q": (0, 0),
                    "k": (0, self.size - 1)
                }
            }[self.board[x][y].color]
            for side, rook_position in rook_initial_positions.items():
                if (x, y) == rook_position:
                    if self.castling[self.board[x][y].color][side]:
                        move.delta_castling[self.board[x]
                                            [y].color][side] = False
                    self.castling[self.board[x][y].color][side] = False

        if self.board[x][y].type == 'k':
            if abs(y2-y) == 2:
                self.board[x2][y2] = self.board[x][y]
                self.board[x][y] = None
                direction = (y2 - y)//2
                rook_y = self.size-1 if direction > 0 else 0
                rook_y2 = y2 - direction
                self.board[x2][rook_y2] = self.board[x2][rook_y]
                self.board[x2][rook_y] = None
                move.moved_pieces.append(
                    [self.board[x2][rook_y2], (x2, rook_y), (x2, rook_y2)])
            else:
                if self.board[x2][y2]:
                    move.captured_pieces.append([self.board[x2][y2], (x2, y2)])
                self.board[x2][y2] = self.board[x][y]
                self.board[x][y] = None

        elif self.board[x][y].type == "p" and self.enpassant == (x2, y2):
            self.board[x2][y2] = self.board[x][y]
            self.board[x][y] = None
            move.captured_pieces.append([self.board[x][y2], (x, y2)])
            self.board[x][y2] = None
        else:
            if self.board[x2][y2]:
                move.captured_pieces.append([self.board[x2][y2], (x2, y2)])
            self.board[x2][y2] = self.board[x][y]
            self.board[x][y] = None

        if promotion_piece:
            self.board[x2][y2].type = promotion_piece
            move.promotion_piece = promotion_piece

        if self.board[x2][y2].type == "p" and abs(x2 - x) == 2:
            self.enpassant = ((x2 + (x-x2)//2, y))
            move.delta_enpassant_square = self.enpassant
        else:
            if self.enpassant:
                move.delta_enpassant_square = self.enpassant
            self.enpassant = None
        self.moves.append(move)

    def find_piece(self, type_of_piece, color_of_piece):
        for x in range(self.size):
            for y in range(self.size):
                piece = self.board[x][y]
                if piece and piece.type == type_of_piece and piece.color == color_of_piece:
                    return(x, y)

    def is_check(self, player=None):
        if not player:
            player = self.current_player
        king_position = self.find_piece("k", player)
        return king_position in self.get_attacking_squares("W" if player == "B" else "B")

    def is_checkmate(self, player=None):
        if not player:
            player = self.current_player
        if not self.is_check(player):
            return False
        for x, y in self.get_pieces(player):
            for move_x, move_y in Piece.moves(self, (x, y)):
                if self.board[x][y].type == "p" and (x == 0 or x == self.size-1):
                    self.make_move((x, y), (move_x, move_y), "q")
                else:
                    self.make_move((x, y), (move_x, move_y), None)
                if not self.is_check(player):
                    self.undo_move()
                    return False
                self.undo_move()
        return True

    def get_attacking_squares(self, player=None):
        if not player:
            player = self.current_player
        pieces = self.get_pieces(player)
        attacking_squares = set()
        for piece_position in pieces:
            attacking_squares.update(Piece.path(self, piece_position))
        return attacking_squares


if __name__ == "__main__":
    board = Board()
    board.setup_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    #board.setup_fen("r4K2/3P4/8/2k5/8/8/8/8 w - - 0 1")
    board.print_board()
    while not board.is_checkmate():
        print(f"Pinned pieces: {board.get_pinned_piece_positions()}")
        board.make_move(*board.input_move())
        board.switch_player()
        board.print_board()
