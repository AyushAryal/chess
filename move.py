from dataclasses import dataclass, field


@dataclass
class Move:
    delta_castling = {"W": {}, "B": {}}
    delta_enpassant_square =  None
    moved_pieces : list = field(default_factory=lambda: [])
    captured_pieces : list = field(default_factory=lambda: [])
    promotion_piece = None
