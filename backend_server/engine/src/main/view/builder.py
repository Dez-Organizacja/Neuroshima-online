from main.state.context import ActionContext
from main.view.state import StateViewBuilder
from main.view.step import StepViewBuilder
from main.rules.game import GameRules

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
            faction : GameRules.get_score(ctx.board, faction)
            for faction in ctx.state.factions
        }

    def build(self, ctx : ActionContext) -> dict:
        return {
            "state"  : self.state_view.build(ctx.state),
            "scores" : self.get_scores(ctx),
            "winner" : GameRules.get_winner(ctx.board, ctx.state.factions),
            "LastClickedHex" : self.build_last_clicked_hex_view(ctx.state),
            "phase"  : ctx.state.phase.value,
            **self.step_view.build_step(ctx).to_dict(),
        }
