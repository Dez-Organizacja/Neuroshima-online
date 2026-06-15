from main.workflows.data import  WorkflowInstance
from main.workflows.factory import WorkflowFactory
from copy import deepcopy
from .scenarios.data import Scenario, StepCase
from main.state.context import ActionContext
from main.state.game_state import GameState
from main.utils.diff_state import DiffState
from main.rules.faction_manager import FactionManager

class WorkflowTester:
    def apply_changes(self, before : ActionContext, step_case : StepCase):
        # print("GETTING EXPECTED STATE")
        expected_ctx = before
        for key, value in step_case.data_delta.items():
            # print(f"changing value of key {key} to {value}")
            setattr(expected_ctx.workflow_data, key, value)

        if step_case.faction_delta is not None:
            expected_ctx.faction = step_case.faction_delta
            # print("nie None")
        
        # print(f"step case turn faction delta {step_case.turn_faction_delta}")
        if step_case.turn_faction_delta is not None:
            # print("turn faction is not None")
            expected_ctx.state.turn_faction = step_case.turn_faction_delta
            # print(expected_ctx)
        # print("getting exp ctx finished")
        # return Serializator.to_dict_dataclass(expected_ctx.state)

    def run(self, scenario: Scenario):
        # print("RUNING SECNARIO")
        # print(scenario)
        # print("---------------")
        ctx = ActionContext(
            state = GameState(factions=scenario.factions),
            faction_manager=FactionManager(scenario.factions)
        )
        ctx.state.workflow_stack.append(
            WorkflowInstance(
                name=scenario.name,
                current_step_index= scenario.current_step,
                config=scenario.config,
            )
        )
        ctx.state.turn_faction = ctx.state.factions[0]
        ctx.state.active_faction = ctx.state.factions[0]

        workflow = WorkflowFactory.create(ctx.workflow_instance)
        workflow.build_steps()

        for step_case in scenario.steps:
            print("######################")
            print("procesing step")
            print(step_case)
            print("------------")

            if step_case.setup:
                step_case.setup(ctx)

            before = deepcopy(ctx)
            # print(f"before step exe data state")
            # print(before)

            step = workflow.get_current_step(ctx)

            print("START EXECUTING")
            print(f"action {step_case.action}")
            print(f"wf_instance {ctx.workflow_instance}")
            if step_case.action:
                result = step.execute(ctx, step_case.action)
            else:
                print("WITHOUT ACTION")
                result = step.execute(ctx)
                
            print("END EXECUTING")
            print("after step exe result")
            print(result)

            print(f"expected result")
            print(step_case.expected_result)

            assert result == step_case.expected_result

            # print("after step exe state")
            # print(Serializator.to_dict_dataclass(ctx.state))

            self.apply_changes(before, step_case)
            # print(f"expected ctx\n{expected_state}")
            # current_state = Serializator.to_dict_dataclass(ctx.state)

            DiffState.compare(ctx.state, before.state)
            # assert current_state == expected_state, Diff.compare(current_state, expected_state)

            ctx.workflow_instance.current_step_index += 1