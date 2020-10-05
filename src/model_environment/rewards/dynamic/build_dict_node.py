from src.model_environment.rewards.node import RewardNode

class BuildDictNode:
    def decode_node_params(self, **params):
        dict_params, rewardnode = {}, None
        for key, value in params.items():
            if key == 'rewardnode':
                rewardnode = RewardNode(**value)
            else:
                dict_params[key] = value
        return dict_params, rewardnode
            
            
