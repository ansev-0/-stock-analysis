from src.model_environment.rewards.node import RewardNode

class BuildNode:

    def decode_node_params(self, **params):
        return {key : RewardNode(**value) if 'rewardnode' in key
                else value 
                for key, value in params.items()}