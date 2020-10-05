from src.model_environment.rewards.not_depend_on_inventory.reward import NotDependOnInventoryReward
from src.tools.pandas_tools import monotic_blocks
import numpy as np
import pandas as pd

class MonoticCumulativeRewards(NotDependOnInventoryReward):

    def __init__(self, 
                 time_values=None,
                 time_values_cache=None, 
                 commision=None, 
                 gamma_pos_not_actions=1, 
                 rewardnode=None):
                 
        super().__init__(rewardnode)
        self._mapper_action_rewards = None
        self._time_values = time_values
        self._commision = commision
        self._gamma_pos_not_actions = gamma_pos_not_actions
        self._get_mapper_action_rewards()

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

        diff = self.time_values.diff(-1)
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

class MonoticCumulativeRewardsNotAction(MonoticCumulativeRewards):
    def get_reward(self, action, time, *args):
        return super().get_reward(action , time, 1)