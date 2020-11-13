from src.model_environment.rewards.not_depend_on_inventory.rewards.base_rewards import BaseNotDependOnInventoryReward
from src.tools.pandas_tools import monotic_blocks

class MonoticCumulativeRewards(BaseNotDependOnInventoryReward):

    def _get_sell_serie(self):
        diff = self.time_values.diff(-1)
        blocks = monotic_blocks(diff, diff_serie=True)
        return diff[::-1].groupby(blocks, sort=False).cumsum()[::-1].dropna().rename('sell_rewards')

        
class MonoticCumulativeRewardsNotAction(MonoticCumulativeRewards):
    def get_reward(self, action, time, *args):
        return super().get_reward(action , time, 1)

