from dataclasses import dataclass, field
from main.tokens.hand import Hand
from main.workflows.data import WorkflowInstance, WorkflowData
from main.board.board import Board

@dataclass
class FakePlayerState:
    hand : Hand = field(default_factory=Hand)

@dataclass
class FakeContext:
    workflow_instance : WorkflowInstance
    workflow_data : WorkflowData = field(default_factory=WorkflowData)
    player : FakePlayerState = field(default_factory=FakePlayerState)
    board : Board = field(default_factory=Board)
    faction : str = "moloch"

