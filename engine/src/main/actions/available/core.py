from main.actions.available.data import AvailableStructure
from main.actions.available.config import AvActionsConfig
from main.state.contex import ActionContext

class AvailableActions:
    def __init__(self, config : AvActionsConfig):
        self.config = config

    def apply_active_key(self, dict, keys):
        for key in keys:
            dict[key] = True

    def apply_hand(self, hand, hand_result):
        for fraction, idxes in hand_result.items():
            for i in idxes:
                hand[fraction][i] = True


    def get_actions(self, ctx : ActionContext):
        actions = AvailableStructure.build(ctx)
        cfg : AvActionsConfig = self.config
        self.apply_active_key(
            dict=actions.board, 
            keys=cfg.get_positions(ctx)
        )
        self.apply_active_key(
            dict=actions.bottoms, 
            keys=cfg.get_bottoms(ctx)
        )
        self.apply_hand(cfg.get_tokens(ctx))
        return actions