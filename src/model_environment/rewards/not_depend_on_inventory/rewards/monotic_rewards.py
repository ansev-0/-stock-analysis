from src.model_environment.rewards.not_depend_on_inventory.rewards.base_rewards import BaseNotDependOnInventoryReward
from src.tools.pandas_tools import monotic_blocks

class MonoticCumulativeRewards(BaseNotDependOnInventoryReward):

    def _get_sell_serie(self):
        diff = self.time_values.diff(-1)
        blocks = monotic_blocks(diff, diff_serie=True)
        return diff[::-1].groupby(blocks, sort=False).cumsum()[::-1].dropna().rename('sell_rewards')


class LossOpportunityPenaltyRewards(MonoticCumulativeRewards):

    def get_reward(self, time, max_purchases, max_sales, *args, **kwargs):

        try:
            return self.rewardnode(self._get_penalty(time, max_purchases, max_sales)) 
#
        except KeyError as error:
            keys_str = ' or '.join(self.mapper_action_rewards.keys())
            raise KeyError(error, f'You must pass : {keys_str}' )


    def _get_penalty(self, time, max_purchases, max_sales):
        return self._get_negative_penalty(max_purchases, max_sales, time) \
            if self._necessary_penalty(time) else 0


    def _get_negative_penalty(self, max_purchases, max_sales, time):
        
        pos_buy_reward = self._positive_penalty_from_action('buy', time)
        if pos_buy_reward:
            return -pos_buy_reward * max_purchases

        pos_sell_reward = self._positive_penalty_from_action('sell', time)
        if pos_sell_reward:
            return -pos_sell_reward * max_sales

        raise ValueError('Invalid mapper')

    def _positive_penalty_from_action(self, action, time):
        reward = self.mapper_action_rewards[action][time]
        return reward if reward > 0 else False
        
    def _necessary_penalty(self, time):
        return self.mapper_action_rewards['no_action'][time] < 0

        
class MonoticCumulativeRewardsNotAction(MonoticCumulativeRewards):
    def get_reward(self, action, time, *args):
        return super().get_reward(action , time, 1)

