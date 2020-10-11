from src.model_environment.rewards.dynamic.dynamic_node import DynamicNode

class BuildNode:

    def decode_node_params(self, **params):
        return {key : DynamicNode(**value) if 'rewardnode' in key
                else value 
                for key, value in params.items()}