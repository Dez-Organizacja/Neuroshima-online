
class AvailableActionResult():
    def __init__(self, positions=None, bottoms=None, hand=None):
        self.positions = positions or []
        self.bottoms = bottoms or []
        self.hand = hand or {}