import numpy as np
import pandas as pd

def make_rewards(serie, commision=None, gamma=1):
    
    diff = serie.diff(-1)
    signs = np.sign(diff).ffill().mask(lambda sign: sign.eq(0)).ffill()
    blocks = signs.ne(signs.shift()).cumsum()
    
    sell = diff[::-1].groupby(blocks).cumsum()[::-1].rename('sell_rewards')
    buy = sell.mul(-1).rename('buy_rewards')
    
    if commision is not None:
        
        commision_serie = sell.abs().mul(-1).add(commision).rename('commision_rewards')
        buy -= commision
        sell -= commision
        
        if gamma != 1:
            commision_serie = commision_serie.where(commision_serie.gt(0), commision_serie.mul(gamma))
            
        return commision_serie, sell, buy
    
    return sell, buy
