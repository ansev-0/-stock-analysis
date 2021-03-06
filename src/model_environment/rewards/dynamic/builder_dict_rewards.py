from src.model_environment.rewards.dynamic.builder_dict_type import DynamicDictNodeBuilder
from src.model_environment.rewards.dynamic.build_dict_node import BuildDictNode
from src.tools.importer import importer
from src.model_environment.rewards.dict_rewards import DictRewards
from src.tools.reduce_tools import combine_dicts


class BuilderDictRewards(BuildDictNode):

    def __init__(self, builder_with_components=None):
        self._builder_with_components = builder_with_components

    def __call__(self, dict_to_build):
        params, rewardnode = self.decode_node_params(**dict_to_build)
        return DictRewards(

            rewardnode=rewardnode, 
            **{type_reward : DynamicDictNodeBuilder(type_reward, 
                                                    self._builder_with_components).build(module_obj_dict)
                for type_reward, module_obj_dict in params.items()}
        )

