from src.model_environment.actions.actions import StatesActions

class DecodeStatesActionsTask:

    def __call__(self, builder_with_components, dict_states_actions):
        return  builder_with_components(StatesActions, dict_states_actions)