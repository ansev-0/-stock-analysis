from src.train.orders.decode_request.agents.decode_task.epsilon import DecodeEpsilonTask

class DecodeStatesAction:

    _decode_epsilon = DecodeEpsilonTask()

    def __call__(self, dict_states_actions):
        return {key : self._apply_sub_task(value) 
                for key, value in dict_states_actions.items()}

    def _apply_sub_task(self, key, value):
        return self._apply_epsilon_task(value) if 'epsilon' in key else value

    def _apply_epsilon_task(self, dict_epsilon):
        return self._decode_epsilon(dict_epsilon)
        