from dataclasses import dataclass, field


@dataclass
class Move:
    delta_castling : dict = field(default_factory=lambda : {"W": {}, "B": {}})
    delta_enpassant_square : 'typing.Any' =  field(default_factory = lambda : None)
    moved_pieces : list = field(default_factory=lambda: [])
    captured_pieces : list = field(default_factory=lambda: [])
    promotion_piece : 'typing.Any' = field(default_factory = lambda : None)

    def to_long_algebraic(self):
        long_algebraic = ""
        _, initial, final = self.moved_pieces[0]
        initial_x, initial_y = initial
        final_x, final_y = final

        long_algebraic += chr(ord("a")+initial_y) + str(8-(initial_x))
        long_algebraic += chr(ord("a")+final_y) + str(8-(final_x))

        if self.promotion_piece:
            long_algebraic+=self.promotion_piece
        return long_algebraic
        