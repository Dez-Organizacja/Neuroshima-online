from main.state.contex import ActionContext
from main.systems.sieciarze import Sieciarze
from main.systems.boosters import BoosterSolver

class PassiveSystems:
    @staticmethod
    def compute(ctx : ActionContext):
        Sieciarze.compute(ctx.board)
        BoosterSolver.compute(ctx.board)