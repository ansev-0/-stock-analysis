from src.model_environment.rewards.dynamic.reward import BuilderReward

class DecodeRewardTask:
    _reward_builder = BuilderReward()
    def __call__(self, reward_dict):
        return self._reward_builder(reward_dict) if reward_dict else None