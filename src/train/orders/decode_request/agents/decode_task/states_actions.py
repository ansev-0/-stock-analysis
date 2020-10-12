from src.model_environment.actions.actions import StatesActions

class DecodeStatesActionsTask:
    def __call__(self, dict_states_actions):
        return  StatesActions(**dict_states_actions)
