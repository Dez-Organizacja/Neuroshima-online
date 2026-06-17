from main.systems.sieciarze import Sieciarze
from main.systems.boosters import BoosterSolver
from main.board.board import Board
from main.state.player_state import PlayerState

class PassiveSystems:
    @staticmethod
    def compute(board : Board, players : dict[str, PlayerState]):
        print("PASSIVE SYSTEMS RECOMPUTING")
        Sieciarze.compute(board)
        BoosterSolver.compute(board, players)