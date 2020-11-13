from src.model_environment.actions.actions import StatesActions
#from src.train.rl_model.commision.dynamic import DynamicCommision

#class DecodeStatesActionsTask:
#
#    def __call__(self, broker, dict_states_actions, dict_cache):
#        return  StatesActions(**dict_states_actions, 
#                              commision=DynamicCommision()(broker).from_cache_train(dict_cache))

class DecodeStatesActionsTask:

    def __call__(self, builder_with_components, dict_states_actions):
        return  builder_with_components(StatesActions, dict_states_actions)