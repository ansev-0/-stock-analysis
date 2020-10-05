from src.model_environment.rewards.dynamic.builder_dict_type import DynamicDictNodeBuilder
from src.model_environment.rewards.dynamic.build_dict_node import BuildDictNode
from src.tools.importer import importer
from src.model_environment.rewards.dict_rewards import DictRewards
from src.tools.reduce_tools import combine_dicts
import pandas as pd

class BuilderDictRewards(BuildDictNode):

    def __call__(self, dict_to_build):
        params, rewardnode = self.decode_node_params(**dict_to_build)
        return DictRewards(rewardnode=rewardnode, 
                           **combine_dicts(*tuple(
                               DynamicDictNodeBuilder(type_reward).build(module_obj_dict) 
                               for type_reward, module_obj_dict in params.items()
                                                 )
                                          )
                          )
