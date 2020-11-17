from src.model_environment.rewards.node import RewardNode
from src.model_environment.rewards.dict_rewards import DictRewards
from src.model_environment.rewards.errors.is_node import check_valid_rewardnode

class Reward:

    def __init__(self, 
                 dict_rewards=None, 
                 rewardnode=None, 
                 reward_node_current_profit=None, 
                 reward_node_incr_profit=None):


        self.dict_rewards = dict_rewards
        self.reward_node_current_profit = reward_node_current_profit
        self.rewardnode_incr_profit = rewardnode_incr_profit
        self.rewardnode = rewardnode

    @property
    def dict_rewards(self):
        return self._dict_rewards

    @dict_rewards.setter
    @property
    def rewardnode(self):
        return self._rewardnode

    @rewardnode.setter
    def rewardnode(self, rewardnode):
        check_valid_rewardnode(rewardnode)
        self._rewardnode = self._valid_rewardnode(rewardnode)

    @property
    def reward_node_current_profit(self):
        return self._reward_node_current_profit

    @reward_node_current_profit.setter
    def reward_node_current_profit(self, reward_node_current_profit):
        check_valid_rewardnode(reward_node_current_profit)
        self._reward_node_current_profit = self._valid_rewardnode(reward_node_current_profit)


    @property
    def rewardnode_incr_profit(self):
        return self._rewardnode_incr_profit

    @rewardnode_next_profit.setter
    def rewardnode_next_profit(self, rewardnode_next_profit):
        check_valid_rewardnode(rewardnode_next_profit)
        self._rewardnode_next_profit = self._valid_rewardnode(rewardnode_next_profit)

    @rewardnode_incr_profit.setter
    def rewardnode_incr_profit(self, rewardnode_incr_profit):
        check_valid_rewardnode(rewardnode_incr_profit)
        self._rewardnode_incr_profit = self._valid_rewardnode(rewardnode_incr_profit)


    def reset(self):
        if self.dict_rewards is not None:
            self.dict_rewards.reset() 


    def reward(self, current_profit, incr_profit, **kwargs):
        return self.rewardnode(self._reward_from_dict_reward(current_profit=current_profit, **kwargs) + \
                               self._rewardnode_current_profit(current_profit) + \
                               self._rewardnode_incr_profit(incr_profit), 
                             **kwargs)

    def _reward_from_dict_reward(self, **kwargs):
        return self._dict_rewards.total_reward(**kwargs) \
                               if self._dict_rewards is not None else 0

    @staticmethod
    def _check_valid_dict_rewards(dict_reward):
        if not isinstance(dict_reward, DictRewards) and dict_reward is not None:
            raise ValueError(f'You must pass a instance of {DictRewards}')

    @staticmethod
    def _valid_rewardnode(rewardnode):
        return rewardnode if rewardnode is not None \
             else RewardNode()
        