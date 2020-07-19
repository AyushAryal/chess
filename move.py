from dataclasses import dataclass


@dataclass
class Move:
    delta_castling = {"W": {}, "B": {}}
    delta_enpassant_square =  None
    moved_pieces = []
    captured_pieces = []
