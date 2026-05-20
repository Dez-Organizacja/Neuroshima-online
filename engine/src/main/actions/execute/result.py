
class ActionResult():
    def __init__(self, 
        effects=None, 
        interaction_state_changes=None, 
        flow_events=None
    ):
        self.effects = effects or []
        self.interaction_state_changes = interaction_state_changes or []
        self.flow_events = flow_events or []