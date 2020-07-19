class Piece(object):
    def __init__(self, type_, color):
        self.type = type_
        self.color = color

    def get_properties(self):
        return (self.type, self.color)


    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        color_map = {
            "B": {
                "k": "♔", "q": "♕", "r": "♖", "b": "♗", "n": "♘", "p": "♟",
            },
            "W": {
                "k": "♚", "q": "♛", "r": "♜", "b": "♝", "n": "♞", "p": "♙",
            }}
        return color_map[self.color][self.type]

    @staticmethod
    def moves(board_obj, pos):
        # Expects that board[x][y] is a piece
        x, y = pos
        board = board_obj.board
        player = board[x][y].color
        if pos in board_obj.get_pinned_piece_positions():
            return set()

        possible_moves = Piece.path(board_obj, pos)
        if board[x][y].type == 'k':
            removed = board[x][y]
            board[x][y] = None
            attacked_squares = board_obj.get_attacking_squares(
                "W" if removed.color == "B" else "B")
            possible_moves = possible_moves.difference(attacked_squares)
            board[x][y] = removed

            # castling
            eliminated_squares = set()
            for _, y_final in possible_moves:
                if abs(y_final - y) == 2:
                    if board_obj.is_check(player):
                        eliminated_squares.add((x, y_final))
                    direction = (y_final - y)//2
                    if (x, y+direction) in attacked_squares:
                        eliminated_squares.add((x, y_final))

            possible_moves = possible_moves.difference(eliminated_squares)
        else:
            eliminated_squares = set()
            if board_obj.is_check(player):
                for move_x, move_y in possible_moves:
                    board_obj.make_move((x,y), (move_x, move_y))
                    if board_obj.is_check(player):
                        eliminated_squares.add((move_x, move_y))
                    board_obj.undo_move()
            possible_moves = possible_moves.difference(eliminated_squares)

        return possible_moves

    @staticmethod
    def path(board_obj, pos):
        # Expects that board[x][y] is a piece
        board = board_obj.board
        x, y = pos
        type_, _ = board[x][y].get_properties()
        return {
            "p": Piece.pawn_moves,
            "k": Piece.king_moves,
            "n": Piece.knight_moves,
            "r": Piece.ranged_piece_moves,
            "q": Piece.ranged_piece_moves,
            "b": Piece.ranged_piece_moves,
        }[type_](board_obj, pos)

    @staticmethod
    def pawn_moves(board_obj, pos):
        board = board_obj.board
        x, y = pos
        _, color = board[x][y].get_properties()
        direction = -1 if color == "W" else +1
        opponent = "B" if color == "W" else "W"
        options = set()
        if board_obj.within_boundaries(x + direction, y-1) and board[x + direction][y-1] and board[x + direction][y-1].color == opponent:
            options.add((x + direction, y-1))
        if board_obj.within_boundaries(x + direction, y+1) and board[x + direction][y+1] and board[x + direction][y+1].color == opponent:
            options.add((x + direction, y+1))
        if board_obj.within_boundaries(x + direction, y) and not board[x + direction][y]:
            options.add((x + direction, y))
        if (not board[x + direction][y]) and (not board[x + direction*2][y]) and (x == board_obj.size-2 or x == 1):
            options.add((x + direction*2, y))
        if board_obj.enpassant:
            en_x, en_y = board_obj.enpassant
            if abs(en_y-y) == 1 and (x+direction) == en_x:
                options.add((en_x, en_y))
        return(options)

    @staticmethod
    def knight_moves(board_obj, pos):
        board = board_obj.board
        x, y = pos
        options = set()
        choices = ((2, 1), (2, -1), (-2, 1), (-2, -1),
                   (1, 2), (-1, 2), (-1, -2), (1, -2))
        for dx, dy in choices:
            if board_obj.within_boundaries(x+dx, y+dy) and (not board[x+dx][y+dy] or board[x+dx][y+dy].color != board[x][y].color):
                options.add((x+dx, y+dy))
        return options

    @staticmethod
    def king_moves(board_obj, pos):
        board = board_obj.board
        x, y = pos
        options = set()
        choices = ((1, 0), (-1, 0), (0, 1), (0, -1),
                   (1, 1), (1, -1), (-1, 1), (-1, -1))
        for dx, dy in choices:
            if board_obj.within_boundaries(x+dx, y+dy) and (not board[x+dx][y+dy] or board[x+dx][y+dy].color != board[x][y].color):
                options.add((x+dx, y+dy))

        for side, castling_possible in board_obj.castling[board[x][y].color].items():
            if castling_possible:
                y_rook = 0 if side == "q" else board_obj.size - 1
                direction = -1 if side == "q" else 1
                cnt = 0
                for i in range(y+direction, y_rook, direction):
                    if board[x][i]:
                        cnt += 1
                if not cnt:
                    options.add((x, y+direction*2))

        return options

    @staticmethod
    def ranged_piece_moves(board_obj, pos):
        options = set()
        board = board_obj.board
        x, y = pos
        type_, _ = board[x][y].get_properties()
        delta_choices = {
            "r": ((1, 0), (-1, 0), (0, 1), (0, -1)),
            "q": ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)),
            "b": ((1, 1), (1, -1), (-1, 1), (-1, -1)),
        }

        def ranged_moves(board_obj, x, y, delta_choices):
            board = board_obj.board
            options = set()
            for dx, dy in delta_choices:
                for c in range(1, board_obj.size):
                    if board_obj.within_boundaries(x+dx*c, y+dy*c) and (not board[x+dx*c][y+dy*c] or board[x+dx*c][y+dy*c].color != board[x][y].color):
                        options.add((x+dx*c, y+dy*c))
                    if board_obj.within_boundaries(x+dx*c, y+dy*c) and board[x+dx*c][y+dy*c]:
                        break
            return options

        options.update(ranged_moves(
            board_obj, x, y, delta_choices[type_]))
        return options
