from src.model_environment.rewards.dynamic.builder_dict_rewards import BuilderDictRewards
from src.model_environment.rewards.reward import Reward
from src.model_environment.rewards.dynamic.build_node import BuildNode

class BuilderReward(BuildNode):

    def __call__(self, params_dict, builder_with_components=None):
        # Build rewardnodes
        params_dict = self.decode_node_params(**params_dict) 
        # Build DictReward
        params_dict['dict_rewards'] = BuilderDictRewards(builder_with_components)(params_dict['dict_rewards']) \
            if params_dict['dict_rewards'] else None
        # Build Reward
        return Reward(**params_dict) 
