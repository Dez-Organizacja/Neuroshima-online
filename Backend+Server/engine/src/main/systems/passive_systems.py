from main.state.contex import ActionContext
from main.systems.sieciarze import Sieciarze

class PassiveSystems:
    @staticmethod
    def compute(ctx : ActionContext):
        Sieciarze.compute(ctx.board)