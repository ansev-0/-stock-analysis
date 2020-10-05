from src.model_environment.rewards.dynamic.builder_dict_type import DynamicDictNodeBuilder
from src.model_environment.rewards.dynamic.build_dict_node import BuildDictNode
from src.tools.importer import importer
from src.model_environment.rewards.dict_rewards import DictRewards

class BuilderDictRewards(BuildDictNode):

    def __call__(self, dict_to_build):
        params, rewardnode = self.decode_node_params(**dict_to_build)
        return DictRewards(rewardnode=rewardnode, 
                           **{DynamicDictNodeBuilder(type_reward).build(module_obj_dict) 
                              for type_reward, module_obj_dict in params.items()})

dict_rewardnode_not_depend_on_inventory = {'weight' : 0.9, 'bias' : 0.2}
dict_rewardnode_depend_on_inventory = {'weight' : 1.0, 'bias' : 0.2}

dict_not_depend_on_inventory = {'monotic_rewards' : {'MonoticCumulativeRewards' : {'time_values' :range(19)}},

                               'rewardnode' : dict_rewardnode_not_depend_on_inventory}

dict_depend_on_inventory = {'mean_rewards' : {'LastPurchasesMeanReward' : {'init_mean_inventory' :0,
                                                                          'init_n_stocks' : 0}},

                               'rewardnode' : dict_rewardnode_not_depend_on_inventory}

dict_rewardnode = {'weight' : 1.0, 'bias' : 0.2}
dict_rewards = {'not_depend_on_inventory' : dict_not_depend_on_inventory,
                'depend_on_inventory' : dict_depend_on_inventory,
                'rewardnode' : dict_rewardnode}

