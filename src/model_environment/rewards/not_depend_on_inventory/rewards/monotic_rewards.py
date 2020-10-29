from src.model_environment.rewards.not_depend_on_inventory.rewards.base_rewards import BaseNotDependOnInventoryReward
from src.tools.pandas_tools import monotic_blocks

class MonoticCumulativeRewards(BaseNotDependOnInventoryReward):

    def _get_sell_serie(self):
        diff = self.time_values.diff(-1)
        blocks = monotic_blocks(diff, diff_serie=True)
        return diff[::-1].groupby(blocks, sort=False).cumsum()[::-1].dropna().rename('sell_rewards')


class LossOpportunityPenaltyRewards(MonoticCumulativeRewards):

    def get_reward(self, action, time, max_purchases, max_sales):

        try:
            return self.rewardnode(self._get_penalty(action, time, max_purchases, max_sales)) 
#
        except KeyError as error:
            keys_str = ' or '.join(self.mapper_action_rewards.keys())
            raise KeyError(error, f'You must pass : {keys_str}' )

    def _get_penalty(self,  action, time, max_purchases, max_sales):
        return self._get_negative_penalty( max_purchases, max_sales, time) \
            if self._necessary_penalty(action, time) else 0


    def _get_negative_penalty(self, max_purchases, max_sales, time):

        if self.mapper_action_rewards['buy'][time] >= 0:
            return self.mapper_action_rewards['buy'][time] * max_purchases
        elif self.mapper_action_rewards['sell'][time] >= 0:
            return self.mapper_action_rewards['sell'][time] * max_sales

        raise ValueError('Invalid mapper')

    def _necessary_penalty(self, action, time):
        return action == 'no_action' and self.mapper_action_rewards['no_action'][time] < 0


    
        

class MonoticCumulativeRewardsNotAction(MonoticCumulativeRewards):
    def get_reward(self, action, time, *args):
        return super().get_reward(action , time, 1)

