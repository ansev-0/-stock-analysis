from src.model_environment.rewards.dict_node import DictNode
from src.model_environment.rewards.not_depend_on_inventory.reward import NotDependOnInventoryReward
import numpy as np

class DictNotDependOnInventoryReward(DictNode):

    _type_node = (NotDependOnInventoryReward, )

    def total_reward(self, action, time, max_purchases, max_purchases_next_time, max_sales, n_stocks=1, *args, **kwargs):

        rewards = self.get_flatten_reward(action=action,
                                          time=time,
                                          max_purchases=max_purchases, 
                                          max_purchases_next_time=max_purchases_next_time,
                                          max_sales= max_sales,
                                          n_stocks=n_stocks)

        return self.rewardnode(reward=np.sum(rewards), 
                               action=action, 
                               time=time, 
                               max_purchases=max_purchases,
                               max_purchases_next_time=max_purchases_next_time,
                               max_sales=max_sales, 
                               n_stocks=n_stocks, 
                               *args, **kwargs)

    def get_reward(self, action, time, max_purchases, max_purchases_next_time, max_sales, n_stocks=1, *args, **kwargs):
        return  self.get_rewards(action=action,
                                 time=time,
                                 max_purchases=max_purchases, 
                                 max_purchases_next_time=max_purchases_next_time,
                                 max_sales= max_sales,
                                 n_stocks=n_stocks)

    def get_flatten_reward(self, action, time, max_purchases, max_purchases_next_time, max_sales, n_stocks=1, *args, **kwargs):
        return  self.get_flatten_rewards(action=action,
                                         time=time,
                                         max_purchases=max_purchases, 
                                         max_purchases_next_time=max_purchases_next_time,
                                         max_sales= max_sales,
                                         n_stocks=n_stocks)
