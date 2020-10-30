from abc import ABCMeta, abstractproperty
from src.model_environment.rewards.node import RewardNode
from src.model_environment.rewards.errors.is_node import check_valid_rewardnode
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
        check_valid_rewardnode(rewardnode)
        self._rewardnode = rewardnode if rewardnode is not None else RewardNode()

