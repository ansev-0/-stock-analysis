from src.model_environment.rewards.node import RewardNode

class BuildNode:

    def decode_node_params(self, **params):
<<<<<<< HEAD
        return {key : RewardNode(**value) if key == 'rewardnode'
=======
        return {key : RewardNode(**value) if 'rewardnode' in key
>>>>>>> ee145a6a2fdce0a7c8f4eea604abe763799e0474
                else value 
                for key, value in params.items()}