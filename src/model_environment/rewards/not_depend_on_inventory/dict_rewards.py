from src.model_environment.rewards.dict_node import DictNode
from src.model_environment.rewards.not_depend_on_inventory.reward import NotDependOnInventoryReward
import numpy as np

class DictNotDependOnInventoryReward(DictNode):

    _type_node = (NotDependOnInventoryReward, )

    def total_reward(self, action, time, n_stocks=1, *args, **kwargs):
        rewards = self.get_flatten_reward(action, time, n_stocks=1)
        return self.rewardnode(np.sum(rewards), action, time, n_stocks=1, *args, **kwargs)

    def get_reward(self, action, time, n_stocks=1, *args, **kwargs):
        return  self.get_rewards(action, time, n_stocks)

    def get_flatten_reward(self, action, time, n_stocks=1, *args, **kwargs):
        return  self.get_flatten_rewards(action, time, n_stocks)
