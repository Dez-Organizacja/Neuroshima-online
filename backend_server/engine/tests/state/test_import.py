import json

from main.main import Game
from main.state.game_state import GameState
from main.workflows.data import WorkflowInstance, WorkflowConfig, WorkflowName
from main.attacks.data import AttackType

def test_game_state_serialization_roundtrip():

    # GIVEN
    state = GameState(
        factions=["moloch", "borgo"],
        turn_faction="moloch"
    )

    state.add_player("moloch")
    state.add_player("morgo")
    state.board.put_token((1, 1), "klaun", "moloch")
    
    state.workflow_stack.append(
        WorkflowInstance(
            name=WorkflowName.TURN,
            config=WorkflowConfig(faction="borgo"),
            current_step_index=2
        )
    )

    # WHEN
    data = state.to_dict()
    json_string = json.dumps(data)
    # print(json_string)
    # assert False

    # # THEN
    loaded_data = json.loads(json_string)

    restored_state : GameState = GameState.from_dict(loaded_data)
    restored_data = restored_state.to_dict()

    assert restored_data == data


def test_game_can_reimport_exported_state_after_placing_token():
    game = Game({"factions": ["moloch", "hegemonia"]})
    game.start_game()

    game = Game(game.export())
    game.handle_action({"type": "hand", "slot": 0})

    game = Game(game.export())
    game.handle_action({"type": "board", "pos": [2, 4]})

    game = Game(game.export())
    view = game.build_user_view()

    assert view["state"]["board"] == [
        {
            "pos": [2, 4],
            "unit": {
                "faction": view["uiState"]["faction"],
                "name": "sztab",
                "rotation": 0,
                "wired": False,
                "ability_used": False,
                "damage": 0,
                "wounds" : 0,
            },
        }
    ]
    assert view["state"]["hands"][view["uiState"]["faction"]]["tokens"] == []
    assert view["uiState"]["mode"] == "rotation"
    assert view["availableActions"]["board"] == [[2, 4]]


# def test_game_state_serialization_preserves_battle_initiative_state():

#     # GIVEN
#     state = GameState(
#         factions=["moloch", "borgo"],
#         current_faction="moloch"
#     )
#     state.board.put_token((2, 4), "klaun", "moloch")
#     token = state.board.get_token((2, 4))
#     token.clever_initiative.num_of_new = 1
#     token.clever_initiative.end_booster_faze()

#     assert token.get_attacks(2) == {
#         AttackType.MELEE: [[0, 1], [5, 1]],
#     }

#     # WHEN
#     data = state.to_dict()
#     restored_state = GameState.from_dict(json.loads(json.dumps(data)))
#     restored_token = restored_state.board.get_token((2, 4))

#     # THEN
#     assert restored_token.clever_initiative.export_state() == token.clever_initiative.export_state()
#     assert restored_token.get_attacks(2) == {}
#     assert restored_token.get_attacks(1) == {
#         AttackType.MELEE: [[0, 1], [5, 1]],
#     }

#     restored_token.clever_initiative.begin_iniciative()

#     assert restored_token.clever_initiative.export_iniciative() == [[2, False, True]]
