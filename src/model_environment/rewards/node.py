from src.model_environment.rewards.errors.node import check_valid_function, check_valid_parameter
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
        check_valid_function(function)
        self._function = function if function is not None else\
             lambda reward, *args, **kwargs: reward

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, weight):
        check_valid_parameter(weight)
        self._weight = weight
        
    @property
    def bias(self):
        return self._bias

    @bias.setter
    def bias(self, bias):
        check_valid_parameter(bias)
        self._bias = bias
