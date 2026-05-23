from main.input.data import ActionType, Bottom
from enum import Enum

class Key(Enum):
    POS = "pos"
    SLOT = "slot"
    NAME = "name"
    ROTATION = "rotation"
    TYPE = "type"

class FormatValidator():
    def __init__(self):
        self.validate_handlers = {
            ActionType.BOARD : self.validate_board_format,
            ActionType.HAND : self.validate_hand_format,
            ActionType.BOTTOM : self.validate_bottom_format,
            ActionType.ROTATE : self.validate_rotate_format
        }

    def validate_board_format(self, action) -> bool:
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

    def validate_hand_format(self, action) -> bool:
        slot = action.get(Key.SLOT, None)
        if(not isinstance(slot, int)):
            return False
        
        return True
        # return game.available_actions[UI.HAND][game.current_fraction][slot]

    def validate_bottom_format(self, action) -> bool:
        name = action.get(Key.NAME, None)
        return name in Bottom
        # return game.available_actions[UI.BOTTOM][name]

    def validate_rotate_format(self, action):
        rotation = action.get(Key.ROTATION, None)
        return isinstance(rotation, int)

    def is_valid_action(self, action) -> bool:
        if (action is None):
            return True
        type = action.get(Key.TYPE, None)
        function = self.validate_handlers.get(type, None)
        if(function is None):
            return False
        return function(action)
