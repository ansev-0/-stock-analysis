from src.model_environment.rewards.dynamic.reward import BuilderReward

class DecodeRewardTask:
    _builder_reward = BuilderReward()
        
    def __call__(self, reward_dict, builder_with_components):
        return self._builder_reward(reward_dict, builder_with_components) if reward_dict else None