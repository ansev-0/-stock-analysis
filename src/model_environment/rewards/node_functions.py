import numpy as np

def risk_by_transaction_size(reward, frac=None, exp=1.15, max_value=0.2,  *args, **kwargs):

    return reward * (1 - np.sign(reward) *  (frac ** exp) + max_value)
