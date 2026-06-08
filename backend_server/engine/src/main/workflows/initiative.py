from main.workflows.base import Workflow
from main.workflows.data import (
    WorkflowConfig,
    WorkflowName, 
    BATTLE_ABILITY_WORKFLOW_REGISTRY
)
from main.board.query import BoardQuery
from main.rules.predicates import(
    token_predicate,
    NOT,
    is_empty_at,
)
from main.state.contex import ActionContext
from main.events.workflow import PushWorkflow
from main.events.data import Event
from main.steps.config import ResolveStepConfig, InitStepConfig
from main.events.effects import (
    EnqueueAttacksEffect,
    ResolveUnitsDamageEffect,
    MarkActivatedUnitsEffect,
)
from main.attacks.data import DirectedIntent
from main.workflows.step_builders import build_end_step
from main.systems.combat import CombatSystem

class InitiativeWorkflow(Workflow):
    def __init__(self, config : WorkflowConfig):
        super().__init__()
        self.initiative = config.initiative
        self.factions = config.factions


    def resolve_battle_abilites(self, ctx : ActionContext) -> list[Event]:
        positions = [
            pos   
            for pos in CombatSystem.get_activating_positions(ctx.board, self.initiative)
            if ctx.board.get_token(pos).has_battle_ability
        ]
        
        result = [
            MarkActivatedUnitsEffect(
                positions=positions, 
                initiative=self.initiative
            )
        ]
        for pos in positions:
            ability = ctx.board.get_token(pos).get_battle_ability()
            wf_name = BATTLE_ABILITY_WORKFLOW_REGISTRY[ability]
            effect = PushWorkflow(name=wf_name, config=WorkflowConfig(pos=pos))
            result.append(effect)
        return result
    
    def build_decisions_step(self):
        return ResolveStepConfig(resolve_func=self.resolve_battle_abilites)


    def enqueue_attacks(self, ctx : ActionContext) -> list[Event]:
        board = ctx.board
        positions = CombatSystem.get_activating_positions(board, self.initiative)
        attack_intents = [
            CombatSystem.build_attack_intent(attack, pos)
            for pos in positions
            for attack in board.get_token(pos).get_attacks()
        ]

        return [
            EnqueueAttacksEffect(attack_intents),
            MarkActivatedUnitsEffect(
                positions=positions,
                initiative=self.initiative
            )
        ]

    def build_attacks_gathering(self):
        return ResolveStepConfig(resolve_func=self.enqueue_attacks)

    def build_healer_setp(self, faction : str):
        return InitStepConfig(
            wf_name=WorkflowName.HEAL,
            wf_config=WorkflowConfig(faction=faction),
        )
    
    def resolve_func(self, ctx : ActionContext):
        return [
            ResolveUnitsDamageEffect(
                positions=BoardQuery([
                    NOT(is_empty_at)
                ]).apply(ctx.board)
            )
        ]

    def _build_steps(self):
        steps = [
            self.build_decisions_step(),
            self.build_attacks_gathering(),
        ] 
        for faction in self.factions:
            steps.append(self.build_healer_setp(faction))

        steps.append(build_end_step(self.resolve_func))
        return steps