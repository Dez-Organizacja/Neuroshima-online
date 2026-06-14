from main.workflows.base import Workflow
from main.workflows.data import WorkflowConfig, WorkflowName
from main.events.flow import GameOverEvent

class EndGameSequenceWorkflow(Workflow):
    def __init__(self, config : WorkflowConfig):
        super().__init__()
        self.factions = config.factions

    def build_player_turn_step(self, faction : str):
        return self.build_push_workflow_step(
            name=WorkflowName.TURN,
            config=WorkflowConfig(faction=faction)
        )

    def _build_steps(self):
        turns = [
            self.build_player_turn_step(faction)
            for faction in self.factions
        ]
        # print("turns step config")    
        # print(turns)
        battle = self.build_push_workflow_step(
                name=WorkflowName.BATTLE,
                config=WorkflowConfig(factions=self.factions) 
            )
        # print(f"battle step config")
        # print(battle)
        return [
            self.build_player_turn_step(self.factions[1]), 
            # bo pierwszy gracz zapoczątkował, więc on dokończył swoją turę
            battle,
            self.build_end_game_check_step(),
            *turns,
            battle,
            self.build_end_game_step(),
        ]