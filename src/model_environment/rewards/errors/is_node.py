from src.model_environment.rewards.node import RewardNode

def check_valid_rewardnode(rewardnode):
    if  rewardnode is not None and  not isinstance(rewardnode, RewardNode):
        raise ValueError(f'You must pass a instance of {RewardNode}')


