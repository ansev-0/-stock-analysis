from src.model_environment.rewards.not_depend_on_inventory.reward import NotDependOnInventoryReward
from pandas import to_datetime
import numpy as np
class PeriodicCurrentProfitReward(NotDependOnInventoryReward):

    def __init__(self, 
                 time_values=None,
                 rewardnode=None):
                 
        super().__init__(rewardnode)

        self._time_values = time_values
        self._mapper_action_rewards = self._get_mapper_action_rewards()
        

    def mapper_action_rewards(self):
        return self._mapper_action_rewards

    def get_reward(self, time, current_profit, *args, **kwargs):

        try:
            return self.rewardnode(self._mapper_action_rewards(time, current_profit)) 

        except Exception as error:
            raise KeyError(error, 'You must pass valid time')


    def _get_mapper_action_rewards(self):
        index = to_datetime(self._time_values.index)
        index_roll = np.roll(index, 1)
        index_roll[0] = index[0]
        index_roll = to_datetime(index_roll)
        new_month = index.month != index_roll.month
        return lambda time, current_profit: current_profit if new_month[time] else 0


