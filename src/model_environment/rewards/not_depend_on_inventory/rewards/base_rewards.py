from src.model_environment.rewards.not_depend_on_inventory.reward import NotDependOnInventoryReward
from src.train.database.cache.agents.find import FindAgentTrainCache
from abc import ABCMeta, abstractmethod
import numpy as np
import pandas as pd

class BaseNotDependOnInventoryReward(NotDependOnInventoryReward, metaclass=ABCMeta):

    def __init__(self, 
                 time_values=None,
                 commision=None, 
                 rewardnode=None):
                 
        super().__init__(rewardnode)

        self._commision = commision
        self._mapper_action_rewards = None
        self._time_values = time_values
        self._get_mapper_action_rewards()

    @abstractmethod
    def _get_sell_serie(self):
        pass

    @property
    def mapper_action_rewards(self):
        return self._mapper_action_rewards

    @property
    def time_values(self):
        return self._time_values

    @time_values.setter
    def time_values(self, time_values):
        self._time_values = time_values
        self._get_mapper_action_rewards()

    @property
    def commision(self):
        return self._commision


    def _get_mapper_action_rewards(self):

        sell = self._get_sell_serie()
        buy = sell.mul(-1).rename('buy_rewards')
        mapper = self._get_dict_mapper(sell.values, buy.values)

        self._mapper_action_rewards = lambda action, time, n_stocks: mapper[action][time] * n_stocks - \
            self._commision(n_stocks=n_stocks, 
                            stock_price=self.time_values[time], 
                            time=time) if action != 'no_action' else 0

    @staticmethod
    def _get_dict_mapper(*args):
        return dict(zip(('sell', 'buy'),
                        args))
