from src.model_environment.rewards.not_depend_on_inventory.rewards.monotic_rewards import MonoticCumulativeRewards
from src.model_environment.rewards.not_depend_on_inventory.rewards.next_incr_rewards import NextIncrRewards

class LossOpportunityPenaltyRewards(MonoticCumulativeRewards):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



    def get_reward(self, time, max_purchases, max_purchases_next_time, *args, **kwargs):

        try:
            return self.rewardnode(self._get_penalty(time, max_purchases, max_purchases_next_time)) 
#
        except KeyError as error:
            keys_str = ' or '.join(self.mapper_action_rewards.keys())
            raise KeyError(error, f'You must pass : {keys_str}' )


    def _get_penalty(self, time, max_purchases, max_purchases_next_time):
        neccesary_penalty_cum_at_time = self._necessary_unit_penalty(time, max_purchases)
        return neccesary_penalty_cum_at_time - self._buy_next_time_reward_pos(time, max_purchases_next_time) \
            if  neccesary_penalty_cum_at_time else 0

    def _necessary_unit_penalty(self, time, max_purchases):
        reward_buy = self._mapper_action_rewards('buy', time, max_purchases)
        return reward_buy if reward_buy > 0 else False


    def _buy_next_time_reward_pos(self, time, max_purchases_next_time):
        buy_next_reward = self._mapper_action_rewards('buy', time + 1, max_purchases_next_time)
        return buy_next_reward if buy_next_reward > 0 else 0