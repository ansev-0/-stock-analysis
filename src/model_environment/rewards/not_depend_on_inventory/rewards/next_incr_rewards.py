from src.model_environment.rewards.not_depend_on_inventory.rewards.base_rewards import BaseNotDependOnInventoryReward

class NextIncrRewards(BaseNotDependOnInventoryReward):

    def _get_sell_serie(self):
        return self.time_values.diff(-1).dropna().rename('sell_rewards')
        
class NextIncrRewardsNotAction(NextIncrRewards):
    def get_reward(self, action, time, *args):
        return super().get_reward(action , time, 1)