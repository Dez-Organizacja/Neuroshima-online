from main.systems.sieciarze import Sieciarze
from main.systems.boosters import BoosterSolver
from main.board.board import Board

class PassiveSystems:
    @staticmethod
    def compute(board : Board):
        print("PASSIVE SYSTEMS RECOMPUTING")
        Sieciarze.compute(board)
        BoosterSolver.compute(board)