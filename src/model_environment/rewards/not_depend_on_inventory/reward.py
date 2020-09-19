from abc import ABCMeta, abstractproperty
from src.model_environment.rewards.node import RewardNode, DictNode
import numpy as np

class NotDependOnInventoryReward(metaclass=ABCMeta):

    def __init__(self, rewardnode=None):
        self.rewardnode = rewardnode

    @abstractproperty
    def mapper_action_rewards(self):
        pass

    def get_reward(self, action, time, n_stocks):
        try:
            return self.rewardnode(self.mapper_action_rewards[action][time] * n_stocks) 

        except KeyError as error:
            keys_str = ' or '.join(self.mapper_action_rewards.keys())
            raise KeyError(error, f'You must pass : {keys_str}' )

    @property
    def rewardnode(self):
        return self._rewardnode

    @rewardnode.setter
    def rewardnode(self, rewardnode):
        self._check_valid_rewardnode(rewardnode)
        self._rewardnode = rewardnode if rewardnode is not None else RewardNode()

        

    @staticmethod
    def _check_valid_rewardnode(rewardnode):
        if  rewardnode is not None and  not isinstance(rewardnode, RewardNode):
            raise ValueError(f'You must pass a instance of {RewardNode}')




class DictNotDependOnInventoryReward(DictNode):
    
    def __init__(self, rewardnode=None):
        super().__init__(NotDependOnInventoryReward, rewardnode=rewardnode)

    def total_reward(self, action, time, n_stocks=1, *args, **kwargs):
        rewards = self.get_flatten_reward(action, time, n_stocks=1)
        return self.rewardnode(np.sum(rewards), action, time, n_stocks=1, *args, **kwargs)

    def get_reward(self, action, time, n_stocks=1, *args, **kwargs):
        return  self.get_rewards(action, time, n_stocks)

    def get_flatten_reward(self, action, time, n_stocks=1, *args, **kwargs):
        return  self.get_flatten_rewards(action, time, n_stocks)



