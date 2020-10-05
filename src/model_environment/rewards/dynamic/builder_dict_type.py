from src.model_environment.rewards.dynamic.rewards import DynamicRewards
from src.tools.importer import importer
from src.tools.reduce_tools import combine_dicts
from src.model_environment.rewards.dynamic.build_dict_node import BuildDictNode

class DynamicDictNodeBuilder(BuildDictNode):

    base_package = 'src.model_environment.rewards'
    def __init__(self, type_reward):
        
        self._module = None
        self._name = None
        self._dynamic_reward = DynamicRewards(type_reward)
        self.type_reward = type_reward
        

    @property
    def type_reward(self):
        return self._dynamic_reward._type_reward
    
    @type_reward.setter
    def type_reward(self, type_reward):
        self._module = f'{self.base_package}.{type_reward}.dict_rewards'
        self._dynamic_reward.type_reward = type_reward
        self._name = self._get_name(type_reward)

    @property
    def name(self):
        return self._name

    @property
    def dict_node_class(self):
        return getattr(importer(self._module), self._name)

    def build(self, module_obj_dict):
        params, rewardnode = self.decode_node_params(**module_obj_dict)
        return self.dict_node_class(
            rewardnode=rewardnode, 
            **combine_dicts(*self._dynamic_reward.\
                            from_many_modules(params).values())
        )

    def _get_name(self, type_reward):
        name = ''.join(map(lambda string: string.capitalize(), 
                           type_reward.split('_'))
                      )
        return f'Dict{name}Reward'
