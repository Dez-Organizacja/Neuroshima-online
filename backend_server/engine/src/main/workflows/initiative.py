from main.workflows.base import Workflow
from main.workflows.data import (
    WorkflowConfig,
    WorkflowName, 
)
from main.systems.combat import CombatSystem
from main.state.contex import ActionContext

class InitiativeWorkflow(Workflow):
    def __init__(self, config : WorkflowConfig):
        super().__init__()
        self.initiative = config.initiative
        self.factions = config.factions

    
    # def build_damage_resolve_step(self):
    #     return InitStepConfig(
    #         wf_name=WorkflowName.DAMAGE_RESOLVE,
    #         wf_config=WorkflowConfig(factions=self.factions)
    #     )

    def resolve_attack_declaration(self, ctx : ActionContext):
        return CombatSystem.resolve_attack_declaration(ctx, self.initiative)

    def _build_steps(self):
        return [
            self.build_resolve_step(self.resolve_attack_declaration),
            self.build_push_workflow_step(
                name=WorkflowName.DAMAGE_RESOLVE,
                config=WorkflowConfig(factions=self.factions),
            ),
            self.build_end_step(),
        ]
            # build_resolve_step(self.resolve_attack_declaration),
            # self.build_damage_resolve_step(),
            # build_end_step(),