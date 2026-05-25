from main.state.contex import ActionContext

class StateViewBuilder:
    @staticmethod
    def build_hands_view(ctx : ActionContext):
        return {
            fraction : ctx.state.players[fraction].hand.to_list()
            for fraction in ctx.state.fractions
        }

    def build(self, ctx : ActionContext):
        return {
            "fractions" : ctx.state.fractions,
            "board" : ctx.board.to_dict(),
            "hands" : self.build_hands_view(ctx)
        }