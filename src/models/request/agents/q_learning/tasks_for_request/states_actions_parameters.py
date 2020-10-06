class TaskStatesActionParameters:
    def __call__(self, states_action_parameters_dict, id_cache):
        return dict(states_action_parameters_dict, **{'id_cache' : id_cache})