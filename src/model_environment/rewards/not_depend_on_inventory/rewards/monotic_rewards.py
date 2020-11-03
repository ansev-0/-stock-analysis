from src.model_environment.rewards.not_depend_on_inventory.rewards.base_rewards import BaseNotDependOnInventoryReward
from src.tools.pandas_tools import monotic_blocks

class MonoticCumulativeRewards(BaseNotDependOnInventoryReward):

    def _get_sell_serie(self):
        diff = self.time_values.diff(-1)
        blocks = monotic_blocks(diff, diff_serie=True)
        return diff[::-1].groupby(blocks, sort=False).cumsum()[::-1].dropna().rename('sell_rewards')

class LossOpportunityPenaltyRewards(MonoticCumulativeRewards):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._penalty_reward = self._time_values.diff(-1).dropna().values
        self._buy_cum_rewards = self.mapper_action_rewards['buy']

    def get_reward(self, time, max_purchases, *args, **kwargs):

        try:
            return self.rewardnode(self._get_penalty(time, max_purchases)) 
#
        except KeyError as error:
            keys_str = ' or '.join(self.mapper_action_rewards.keys())
            raise KeyError(error, f'You must pass : {keys_str}' )


    def _get_penalty(self, time, max_purchases):
        return max_purchases * self._penalty_reward[time] \
            if self._necessary_unit_penalty(time) else 0

    def _necessary_unit_penalty(self, time):
        return self._buy_cum_rewards[time] > 0 


class SellRewards(MonoticCumulativeRewards):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sell_rewards = self._time_values.diff(-1).dropna().values
        self._sell_cum_rewards = self.mapper_action_rewards['sell']

    def get_reward(self, action, time, n_stocks, *args, **kwargs):

        try:
            return self.rewardnode(self._get_sell_reward(action, time, n_stocks)) 
#
        except KeyError as error:
            keys_str = ' or '.join(self.mapper_action_rewards.keys())
            raise KeyError(error, f'You must pass : {keys_str}' )


    def _get_sell_reward(self, action, time, n_stocks):
        return n_stocks * self._sell_rewards[time] \
            if ('action' == 'sell') and (self._sell_cum_rewards[time] > 0) else 0




        
class MonoticCumulativeRewardsNotAction(MonoticCumulativeRewards):
    def get_reward(self, action, time, *args):
        return super().get_reward(action , time, 1)

