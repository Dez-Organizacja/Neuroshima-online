from main.events.data import OnClickData, Event
from main.events.effects import DiscardTokenEffect, MarkAbilityUsedEffect
from main.events.workflow import ConsumeOnClick
from main.workflows.data import WorkflowInstance

class OnClickSystem:
    @staticmethod
    def resolve(wf_instance : WorkflowInstance) -> list[Event]:
        if wf_instance.on_click_consumed:
            return []
        
        effects = [ConsumeOnClick()]
        # print("RESOLVE ON CLICK")
        data = wf_instance.config.on_click
        # print(f"on click data: {data}")
        if data.discard_slot is not None:
            effects.append(DiscardTokenEffect(data.discard_slot))

        if data.mark_activated_pos is not None:
            effects.append(MarkAbilityUsedEffect(data.mark_activated_pos))
        
        return effects