from main.workflows.base import Workflow
from main.workflows.data import WorkflowName, WorkflowConfig
from main.steps.config import InitStepConfig
from main.workflows.step_builders import build_end_step, build_resolve_step
from main.systems.combat import CombatSystem

class ResolveDamageWorkflow(Workflow):
    def __init__(self, config : WorkflowConfig):
        super().__init__()
        self.factions = config.factions

    def build_faction_heal_step(self, faction : str):
        return InitStepConfig(
            wf_name=WorkflowName.HEAL,
            wf_config=WorkflowConfig(faction=faction),
        )

    def _build_steps(self):
        healers = [
            self.build_faction_heal_step(faction)
            for faction in self.factions
        ]
        return [
            build_resolve_step(CombatSystem.resolve_pending_attacks),
            *healers,
            build_end_step(CombatSystem.resolve_combat_damage)
        ]