from abc import ABCMeta, abstractmethod
from src.model_environment.rewards.node import RewardNode
import numpy as np

class DependOnInventoryReward(metaclass=ABCMeta):

    def __init__(self, init_n_stocks, rewardnode=None):

        self._n_stocks = None
        self.rewardnode = rewardnode
        self._init_n_stocks = init_n_stocks
        self.reset()

    @property
    def rewardnode(self):
        return self._rewardnode

    @rewardnode.setter
    def rewardnode(self, rewardnode):
        self._check_valid_rewardnode(rewardnode)
        self._rewardnode = rewardnode if rewardnode is not None else RewardNode()

    @property
    def n_stocks(self):
        return self._n_stocks

    def get_reward(self, *args, **kwargs):
        return self.rewardnode(self._get_reward(*args, **kwargs))

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def _get_reward(self):
        pass


    @staticmethod
    def _check_valid_rewardnode(rewardnode):
        if  rewardnode is not None and  not isinstance(rewardnode, RewardNode):
            raise ValueError(f'You must pass a instance of {RewardNode}')
