from abc import ABCMeta, abstractmethod
from src.model_environment.rewards.node import RewardNode
from src.model_environment.rewards.errors.is_node import check_valid_rewardnode
import numpy as np


class DictNode(dict, metaclass=ABCMeta):

    @property
    @classmethod
    @abstractmethod
    def _type_node(self):
        pass

    def __init__(self, rewardnode=None):
        self.rewardnode = rewardnode

    @property
    def rewardnode(self):
        return self._rewardnode

    @rewardnode.setter
    def rewardnode(self, rewardnode):
        check_valid_rewardnode(rewardnode)
        self._rewardnode = rewardnode if rewardnode is not None else RewardNode()

    def __setitem__(self, reward_name, reward):

        if np.any([isinstance(reward, type_node) 
                   for type_node in  self._type_node]):
            super().__setitem__(reward_name, reward)

        else:
            valid_types = ' or '.join(map(str, self._type_node))
            raise TypeError(f'You must pass an instance of {valid_types}')

    def get_rewards(self, *args, **kwargs):
        return {key : value.get_reward(*args, **kwargs) for key, value in self.items()} 

    def get_flatten_rewards(self, *args, **kwargs):
        return tuple(value.get_reward(*args, **kwargs) for value in self.values())

    def total_rewards(self, *args, **kwargs):
        return np.sum([reward.total_reward(*args, **kwargs) for reward in self.values()])

    

