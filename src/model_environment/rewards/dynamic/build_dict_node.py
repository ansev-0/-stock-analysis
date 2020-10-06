from src.model_environment.rewards.node import RewardNode

class BuildDictNode:
    def decode_node_params(self, **params):
        dict_params, rewardnode = {}, None
        for key, value in params.items():
            if key == 'rewardnode':
                rewardnode = RewardNode(**value)
<<<<<<< HEAD
            dict_params[key] = value
=======
            else:
                dict_params[key] = value
>>>>>>> ee145a6a2fdce0a7c8f4eea604abe763799e0474
        return dict_params, rewardnode
            
            
