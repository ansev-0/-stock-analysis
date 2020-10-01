from abc import ABCMeta, abstractmethod
from inspect import isfunction
import numpy as np

class RewardNode:

    def __init__(self, weight=1, bias=0, function=None):
        self.weight = weight
        self.bias = bias
        self.function = function

    def __call__(self, reward, *args, **kwargs):
        return self.function(reward, *args, **kwargs) * self.weight + self.bias

    @property
    def function(self):
        return self._function  

    @function.setter
    def function(self, function):
        self._check_valid_function(function)
        self._function = function if function is not None else lambda reward, *args, **kwargs: reward

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, weight):
        self._check_valid_parameter(weight)
        self._weight = weight
        
    @property
    def bias(self):
        return self._bias

    @bias.setter
    def bias(self, bias):
        self._check_valid_parameter(bias)
        self._bias = bias


    @staticmethod
    def _check_valid_parameter(parameter):
        if  not isinstance(parameter, float) and  not isinstance(parameter, int):
            raise ValueError('You must pass int or float parameter')

    @staticmethod
    def _check_valid_function(function):
        if  function is not None and  not isfunction(function):
            raise ValueError('You must pass a instance of function')


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
        self._check_valid_rewardnode(rewardnode)
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

    

    @staticmethod
    def _check_valid_rewardnode(rewardnode):
        if  rewardnode is not None and  not isinstance(rewardnode, RewardNode):
            raise ValueError(f'You must pass a instance of {RewardNode}')




