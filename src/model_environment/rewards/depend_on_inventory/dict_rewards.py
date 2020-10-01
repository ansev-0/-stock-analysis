from src.model_environment.rewards.node import DictNode
from src.model_environment.rewards.depend_on_inventory.reward import DependOnInventoryReward
import numpy as np

class DictDependOnInventoryReward(DictNode):

    _type_node = (DependOnInventoryReward, )

    def total_reward(self, action, n_stocks, price, *args, **kwargs):
        rewards = self.get_flatten_reward(action, n_stocks, price)
        return self.rewardnode(np.sum(rewards), *args, **kwargs)

    def get_reward(self, action, n_stocks, price, *args, **kwargs):
        return self.get_rewards(action, n_stocks, price)

    def get_flatten_reward(self, action, n_stocks, price, *args, **kwargs):
        return  self.get_flatten_rewards(action, n_stocks, price)

    def reset(self):
        for depend_on_reward in self.values():
            depend_on_reward.reset()
