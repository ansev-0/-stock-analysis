from src.model_environment.rewards.depend_on_inventory.dict_rewards import DictDependOnInventoryReward
from src.model_environment.rewards.not_depend_on_inventory.dict_rewards import DictNotDependOnInventoryReward
from src.model_environment.rewards.node import DictNode

class DictRewards(DictNode):

    _type_node = (DictDependOnInventoryReward, DictNotDependOnInventoryReward)

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