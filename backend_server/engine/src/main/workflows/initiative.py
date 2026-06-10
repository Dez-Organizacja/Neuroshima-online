from main.workflows.base import Workflow
from main.workflows.data import (
    WorkflowConfig,
    WorkflowName, 
)
from main.steps.config import InitStepConfig
from main.workflows.step_builders import build_end_step, build_resolve_step
from main.systems.combat import CombatSystem
from main.state.contex import ActionContext

class InitiativeWorkflow(Workflow):
    def __init__(self, config : WorkflowConfig):
        super().__init__()
        self.initiative = config.initiative
        self.factions = config.factions

    
    def build_damage_resolve_step(self):
        return InitStepConfig(
            wf_name=WorkflowName.DAMAGE_RESOLVE,
            wf_config=WorkflowConfig(factions=self.factions)
        )

    def resolv_attack_declaration(self, ctx : ActionContext):
        return CombatSystem.resolve_attack_declaration(ctx, self.initiative)

    def _build_steps(self):
        return [
            build_resolve_step(self.resolv_attack_declaration),
            self.build_damage_resolve_step(),
            build_end_step(),
        ]