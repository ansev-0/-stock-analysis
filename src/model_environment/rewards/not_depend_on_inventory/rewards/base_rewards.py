from src.model_environment.rewards.not_depend_on_inventory.reward import NotDependOnInventoryReward
from src.train.database.cache.agents.find import FindAgentTrainCache
from abc import ABCMeta, abstractmethod
import numpy as np
import pandas as pd

class BaseNotDependOnInventoryReward(NotDependOnInventoryReward, metaclass=ABCMeta):

    def __init__(self, 
                 time_values=None,
                 id_cache=None, 
                 commision=0, 
                 gamma_pos_not_actions=1, 
                 rewardnode=None):
                 
        super().__init__(rewardnode)
        self._id_cache = id_cache
        self._commision = commision
        self._mapper_action_rewards = None
        self._time_values = self._init_time_values(time_values)
        self._gamma_pos_not_actions = gamma_pos_not_actions
        self._get_mapper_action_rewards()

    @abstractmethod
    def _get_sell_serie(self):
        pass

    @property
    def id_cache(self):
        return self._id_cache

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

    @commision.setter
    def commision(self, commision):
        self._commision = commision if commision is not None else 0
        self._get_mapper_action_rewards()

    @property
    def gamma_pos_not_actions(self):
        return self._gamma_pos_not_actions

    @gamma_pos_not_actions.setter
    def gamma_pos_not_actions(self, gamma_pos_not_actions):
        self._gamma_pos_not_actions = gamma_pos_not_actions
        self._get_mapper_action_rewards()

    def _get_mapper_action_rewards(self):

        sell = self._get_sell_serie()
        buy = sell.mul(-1).rename('buy_rewards')

        no_actions_serie = sell.abs().mul(-1).add(self.commision).rename('commision_rewards')
        buy -= self.commision
        sell -= self.commision
        no_actions_serie = no_actions_serie.where(no_actions_serie.le(0),
                                                  no_actions_serie.mul(self.gamma_pos_not_actions))
        self._mapper_action_rewards = self._get_dict_mapper(no_actions_serie.values, sell.values, buy.values)

    @staticmethod
    def _get_dict_mapper(*args):
        return dict(zip(('no_action', 'sell', 'buy'),
                        args))

    def _init_time_values(self, time_values):

        if self._id_cache is not None:
            return pd.Series(FindAgentTrainCache().\
                find_by_id(self._id_cache, 
                           projection = {'time_values' : True,
                                         '_id' : False})['time_values'])
        elif time_values is not None:
            return time_values

        raise ValueError('You must pass time_values or id_cache parameters')