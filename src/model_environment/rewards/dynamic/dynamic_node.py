from src.model_environment.rewards.node import RewardNode
from src.model_environment.rewards import node_functions

class DynamicNode(RewardNode):

    def __init__(self, **kwargs):
        super().__init__(**self._modify_function(**kwargs))

    def get_function(self, name):
        return getattr(node_functions, name)

    def _modify_function(self, **kwargs):
        for key, value in kwargs:
            if key == 'function':
                kwargs[key] = self.get_function(key)
        return kwargs
