
from src.model_environment.rewards.node import RewardNode
from src.model_environment.rewards.dict_rewards import DictRewards
from src.model_environment.rewards.errors.is_node import check_valid_rewardnode

class Reward:

    def __init__(self, 
                 dict_rewards, 
                 rewardnode=None, 
                 rewardnode_current_profit=None, 
                 rewardnode_next_profit=None):


        self.dict_rewards = dict_rewards
        self.rewardnode_current_profit = rewardnode_current_profit
        self.rewardnode_next_profit = rewardnode_next_profit
        self.rewardnode = rewardnode

    @property
    def dict_rewards(self):
        return self._dict_rewards

    @dict_rewards.setter
    def dict_rewards(self, dict_rewards):
        self._check_valid_dict_rewards(dict_rewards)
        self._dict_rewards = dict_rewards

    @property
    def rewardnode(self):
        return self._rewardnode

    @rewardnode.setter
    def rewardnode(self, rewardnode):
        check_valid_rewardnode(rewardnode)
        self._rewardnode = self._valid_rewardnode(rewardnode)

    @property
    def rewardnode_current_profit(self):
        return self._rewardnode_current_profit

    @rewardnode_current_profit.setter
    def rewardnode_current_profit(self, rewardnode_current_profit):
        check_valid_rewardnode(rewardnode_current_profit)
        self._rewardnode_current_profit = self._valid_rewardnode(rewardnode_current_profit)


    @property
    def rewardnode_next_profit(self):
        return self._rewardnode_next_profit

    @rewardnode_next_profit.setter
    def rewardnode_next_profit(self, rewardnode_next_profit):
        check_valid_rewardnode(rewardnode_next_profit)
        self._rewardnode_next_profit = self._valid_rewardnode(rewardnode_next_profit)

    def reset(self):
        self.dict_rewards.reset()


    def reward(self, current_profit, next_profit, **kwargs):

        return self.rewardnode(self._dict_rewards.total_reward(**kwargs) + \
                               self._rewardnode_current_profit(current_profit) + \
                               self._rewardnode_next_profit(next_profit), 
                               **kwargs)


    @staticmethod
    def _check_valid_dict_rewards(dict_reward):
        if not isinstance(dict_reward, DictRewards):
            raise ValueError(f'You must pass a instance of {DictRewards}')

    @staticmethod
    def _valid_rewardnode(rewardnode):
        return rewardnode if rewardnode is not None \
             else RewardNode()
        