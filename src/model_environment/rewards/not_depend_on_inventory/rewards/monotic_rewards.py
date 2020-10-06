from src.model_environment.rewards.not_depend_on_inventory.reward import NotDependOnInventoryReward
from src.train.database.cache.agents.find import FindAgentTrainCache
from src.tools.pandas_tools import monotic_blocks
import numpy as np
import pandas as pd

class MonoticCumulativeRewards(NotDependOnInventoryReward):

    def __init__(self, 
                 values_to_make_reward=None,
                 id_cache=None, 
                 commision=None, 
                 gamma_pos_not_actions=1, 
                 rewardnode=None):
                 
        super().__init__(rewardnode)
        self._id_cache = id_cache
        self._mapper_action_rewards = None
        self._values_to_make_reward = self._init_values_to_make_reward(values_to_make_reward)
        self._commision = commision
        self._gamma_pos_not_actions = gamma_pos_not_actions
        self._get_mapper_action_rewards()

    @property
    def id_cache(self):
        return self._id_cache

    @property
    def mapper_action_rewards(self):
        return self._mapper_action_rewards

    @property
    def values_to_make_reward(self):
        return self._values_to_make_reward

    @values_to_make_reward.setter
    def values_to_make_reward(self, values_to_make_reward):
        self._values_to_make_reward = values_to_make_reward
        self._get_mapper_action_rewards()

    @property
    def commision(self):
        return self._commision

    @commision.setter
    def commision(self, commision):
        self._commision = commision
        self._get_mapper_action_rewards()

    @property
    def gamma_pos_not_actions(self):
        return self._gamma_pos_not_actions

    @gamma_pos_not_actions.setter
    def gamma_pos_not_actions(self, gamma_pos_not_actions):
        self._gamma_pos_not_actions = gamma_pos_not_actions
        self._get_mapper_action_rewards()

    def _get_mapper_action_rewards(self):

        diff = self.values_to_make_reward.diff(-1)
        blocks = monotic_blocks(diff, diff_serie=True)
        sell = diff[::-1].groupby(blocks, sort=False).cumsum()[::-1].dropna().rename('sell_rewards')
        buy = sell.mul(-1).dropna().rename('buy_rewards')

        if self.commision is not None:
            no_actions_serie = sell.abs().mul(-1).add(self.commision).rename('commision_rewards')
            buy -= self.commision
            sell -= self.commision
            if self.gamma_pos_not_actions != 1:
                no_actions_serie = no_actions_serie.where(no_actions_serie.gt(0),
                                                            no_actions_serie.mul(self.gamma_pos_not_actions))
            self._mapper_action_rewards = self._get_dict_mapper(no_actions_serie, sell, buy)
        else:
            self._mapper_action_rewards = self._get_dict_mapper(None, sell, buy)

    @staticmethod
    def _get_dict_mapper(*args):
        return dict(zip(('no_action', 'sell', 'buy'),
                        args))

    def _init_values_to_make_reward(self, values_to_make_reward):

        if self._id_cache is not None:
            return pd.Series(FindAgentTrainCache().\
                find_by_id(self._id_cache, 
                           projection = {'values_to_make_reward' : True,
                                         '_id' : False})['values_to_make_reward'])

        elif values_to_make_reward is not None:
            return values_to_make_reward

        raise ValueError('You must pass values_to_make_reward or id_cache parameters')

class MonoticCumulativeRewardsNotAction(MonoticCumulativeRewards):
    def get_reward(self, action, time, *args):
        return super().get_reward(action , time, 1)