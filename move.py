from dataclasses import dataclass, field


@dataclass
class Move:
    delta_castling : dict = field(default_factory=lambda : {"W": {}, "B": {}})
    delta_enpassant_square : 'typing.Any' =  field(default_factory = lambda : None)
    moved_pieces : list = field(default_factory=lambda: [])
    captured_pieces : list = field(default_factory=lambda: [])
    promotion_piece : 'typing.Any' = field(default_factory = lambda : None)