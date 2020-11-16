from src.model_environment.actions.actions import StatesActions

class DecodeStatesActionsTask:

    def __call__(self, dict_states_actions, builder_with_components):
        return  builder_with_components(StatesActions, dict_states_actions)