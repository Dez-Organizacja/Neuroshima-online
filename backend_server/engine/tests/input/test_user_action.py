from main.input.data import UserActionFactory, UserAction, BoardAction

def test_user_action_factory():
    data = {
        "type" : "board",
        "pos" : (1, 1)
    }
    user_action = UserActionFactory.create(data)

    assert isinstance(user_action, BoardAction)
    assert user_action.pos == (1, 1)
    assert user_action.type == "board"