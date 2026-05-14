from main.state.user_action import Type
from enum import Enum
from main.utils.variable import Bottom

class Key(Enum):
    POS = "pos"
    SLOT = "slot"
    NAME = "name"
    ROTATION = "rotation"
    TYPE = "type"

class FormatValidator():
    def __init__(self):
        self.validate_handlers = {
            Type.BOARD : self.validate_board_format,
            Type.HAND : self.validate_hand_format,
            Type.BOTTOM : self.validate_bottom_format,
            Type.ROTATE : self.validate_rotate_format
        }

    def validate_board_format(self, state, action):
        pos = action[Key.POS]
        if(not isinstance(pos, tuple)):
            return False
        if(len(pos) != 2):
            return False
        x, y = pos
        if(not isinstance(x, int) or not isinstance(y, int)):
            return False
        return True
        # return state.available_actions[UI.BOARD][x][y]

    def validate_hand_format(self, state, action):
        slot = action.get(Key.SLOT, None)
        if(not isinstance(slot, int)):
            return False
        
        return True
        # return game.available_actions[UI.HAND][game.current_fraction][slot]

    def validate_bottom_format(self, state, action):
        name = action.get(Key.NAME, None)
        return name in Bottom
        # return game.available_actions[UI.BOTTOM][name]

    def validate_rotate_format(self, state, action):
        rotation = action.get(Key.ROTATION, None)
        return isinstance(rotation, int)

    def is_valid_action(self, state, action):
        if (action is None):
            return True
        type = action.get(Key.TYPE, None)
        function = self.validate_handlers.get(type, None)
        if(function is None):
            return False
        return function(state, action)
