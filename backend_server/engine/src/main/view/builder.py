from main.state.contex import ActionContext
from main.view.state import StateViewBuilder
from main.view.step import StepViewBuilder

class GameViewBuilder:
    def __init__(self):
        self.state_view = StateViewBuilder()
        self.step_view = StepViewBuilder()

    @staticmethod
    def build_last_clicked_hex_view(state) -> dict:
        last_clicked_hex = state.last_clicked_hex
        return {
            "source": last_clicked_hex.source,
            "pos": list(last_clicked_hex.pos) if last_clicked_hex.pos is not None else None,
            "slot": last_clicked_hex.slot,
        }

    @staticmethod
    def get_scores(ctx : ActionContext):
        return {
            faction : ctx.rules.get_score(ctx.board, faction)
            for faction in ctx.state.factions
        }

    def build(self, ctx : ActionContext) -> dict:
        return {
            "state" : self.state_view.build(ctx.state),
            "scores" : self.get_scores(ctx),
            "winner" : ctx.rules.get_winner(ctx.board, ctx.state.factions),
            "lastClickedHex" : self.build_last_clicked_hex_view(ctx.state),
            **self.step_view.build_step(ctx).to_dict(),
        }
