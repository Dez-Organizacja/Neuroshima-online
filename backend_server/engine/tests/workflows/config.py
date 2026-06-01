from main.workflows.data import WorkflowConfig, WorkflowName, WorkflowInstance
from main.state.serialization import Serializator

def test_serialization():
    data = {
      "config" : {
        "factions" : [ "borgo", "moloch" ]
      },
      "current_step_index" : 1,
      "name" : "game"
    }

    # config = Serializator.from_dict_dataclass(WorkflowConfig, data["config"])
    # print(config)
    instance = Serializator.from_dict_dataclass(WorkflowInstance, data)
    expected = WorkflowInstance(
        name = WorkflowName.GAME,
        current_step_index=1,
        config=WorkflowConfig(factions=["borgo", "moloch"])
    )
    print(instance == expected)
    # assert False