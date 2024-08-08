from base_types.types import *

class StateMachine:
    def __init__(self):
        pass
    
    def evaluate(self, s: State, e: Event) -> State:
        s.events_list.append(e)
        pass

    def evaluate_metrics(self, s: State) -> dict:
        pass