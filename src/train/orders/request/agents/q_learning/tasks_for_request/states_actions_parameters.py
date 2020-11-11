class StatesActionParametersTask:
    def __call__(self, states_action_parameters_dict, cache_id):
        return dict(states_action_parameters_dict, **{'cache_id' : cache_id})