from src.model_environment.rewards.depend_on_inventory.reward import DictDependOnInventoryReward
from src.model_environment.rewards.not_depend_on_inventory.reward import DictNotDependOnInventoryReward
from src.model_environment.rewards.node import DictNode, RewardNode

class DictRewards(DictNode):

    def __init__(self, rewardnode=None):
        super().__init__((DictDependOnInventoryReward, DictNotDependOnInventoryReward),
                         rewardnode=rewardnode)

    def total_reward(self,  **kwargs):
        return self.rewardnode(self.total_rewards(**kwargs), **kwargs)

    def get_reward(self, action, **kwargs):
        return self.get_rewards(action, **kwargs)

    def get_flatten_reward(self, action, **kwargs):
        return self.get_flatten_rewards(action, **kwargs)


    def reset(self):
        for reward_dict in self.values():
            if isinstance(reward_dict, DictDependOnInventoryReward):
                reward_dict.reset()

class Reward:

    def __init__(self, dict_rewards, rewardnode=None, rewardnode_profit=None):
        self.dict_rewards = dict_rewards
        self.rewardnode_profit = rewardnode_profit
        self.rewardnode = rewardnode

    @property
    def dict_rewards(self):
        return self._dict_rewards

    @dict_rewards.setter
    def dict_rewards(self, dict_rewards):
        self._check_valid_dict_rewards(dict_rewards)
        self._dict_rewards = dict_rewards

    def reset(self):
        self.dict_rewards.reset()

    @property
    def rewardnode(self):
        return self._rewardnode_profit

    @rewardnode.setter
    def rewardnode(self, rewardnode):
        self._check_valid_rewardnode(rewardnode)
        self._rewardnode = self._valid_rewardnode(rewardnode)


    @property
    def rewardnode_profit(self):
        return self._rewardnode_profit

    @rewardnode_profit.setter
    def rewardnode_profit(self, rewardnode_profit):
        self._check_valid_rewardnode(rewardnode_profit)
        self._rewardnode_profit = self._valid_rewardnode(rewardnode_profit)


    def reward(self, profit, **kwargs):
        return self.rewardnode(self.dict_rewards.total_reward(**kwargs) + self.rewardnode_profit(profit), **kwargs)


    @staticmethod
    def _check_valid_dict_rewards(dict_reward):
        if not isinstance(dict_reward, DictRewards):
            raise ValueError(f'You must pass a instance of {DictRewards}')

    @staticmethod
    def _check_valid_rewardnode(rewardnode):
        if  rewardnode is not None and  not isinstance(rewardnode, RewardNode):
            raise ValueError(f'You must pass a instance of {RewardNode}')

    @staticmethod
    def _valid_rewardnode(rewardnode):
        return rewardnode if rewardnode is not None \
             else RewardNode()
        


    
    

