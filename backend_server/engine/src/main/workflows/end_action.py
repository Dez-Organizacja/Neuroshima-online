from main.workflows.base import Workflow
from main.state.context import ActionContext
from main.events.effects import RecomputePassivesEffect, ResetActionData
from main.events.flow import StartBattleEvent
from main.rules.battle import BattleRules

class EndActionWorkflow(Workflow):

    @staticmethod
    def recompute_passives(ctx : ActionContext):
        return [RecomputePassivesEffect()]

    @staticmethod
    def start_battle_if_needed(ctx : ActionContext):
        if BattleRules.should_start(ctx):
            return [StartBattleEvent()]

    @staticmethod
    def reset_state_execution_data(ctx : ActionContext):
        return [ResetActionData()]

    def _build_steps(self):
        return [
            self.build_resolve_step(
                self.reset_state_execution_data,
                self.recompute_passives,
                self.start_battle_if_needed,
            ),
            self.build_end_step(),
        ]