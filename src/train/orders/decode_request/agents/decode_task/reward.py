from src.model_environment.rewards.dynamic.reward import BuilderReward

class DecodeRewardTask:

    def __init__(self, builder_with_components=None):
        self._reward_builder = BuilderReward(builder_with_components)
        
    def __call__(self, reward_dict):
        return self._reward_builder(reward_dict) if reward_dict else None