from main.workflows.base import Workflow
from main.workflows.data import WorkflowName, WorkflowConfig
from main.systems.combat import CombatSystem

class ResolveDamageWorkflow(Workflow):
    def __init__(self, config : WorkflowConfig):
        super().__init__()
        self.factions = config.factions

    def build_faction_heal_step(self, faction : str):
        return self.build_push_workflow_step(
            name=WorkflowName.HEAL,
            config=WorkflowConfig(faction=faction)
        )
        # return InitStepConfig(
        #     wf_name=WorkflowName.HEAL,
        #     wf_config=WorkflowConfig(faction=faction),
        # )

    def _build_steps(self):
        healers = [
            self.build_faction_heal_step(faction)
            for faction in self.factions
        ]
        return [
            self.build_resolve_step(CombatSystem.resolve_pending_attacks),
            *healers,
            self.build_resolve_step(CombatSystem.resolve_combat_damage),
            self.build_end_step(),
        ]