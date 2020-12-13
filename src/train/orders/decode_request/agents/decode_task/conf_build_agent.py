from src.train.orders.decode_request.agents.decode_task.epsilon import DecodeEpsilonTask
from src.train.interface_epoch.dynamic_interface import DynamicInterface

class DecodeConfBuildAgentTask:

    _decode_epsilon = DecodeEpsilonTask()
    _decode_interface = DynamicInterface()

    def __call__(self, dict_states_actions):
        return {key : self._apply_sub_task(key, value) 
                for key, value in dict_states_actions.items()}

    def _apply_sub_task(self, key, value):
        for task in ('epsilon', 'interface'):
            if task in key:
                return getattr(self, f'_apply_{task}_task')(value) 
        return value

    def _apply_epsilon_task(self, dict_epsilon):
        return self._decode_epsilon(**dict_epsilon)

    def _apply_interface_task(self, dict_interface):
        return self._decode_interface.flatten_interfaces(dict_interface)
        