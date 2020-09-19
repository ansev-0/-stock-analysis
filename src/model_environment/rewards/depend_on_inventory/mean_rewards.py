from src.model_environment.states import States
from src.model_environment.rewards.depend_on_inventory.reward import DependOnInventoryReward


class LastPurchasesMeanReward(DependOnInventoryReward):

    def __init__(self, init_mean_inventory, *args, **kwargs):

        self._mean_inventory = None
        self._init_mean_inventory = init_mean_inventory
        super().__init__(*args, **kwargs)

    #properties
    @property
    def init_mean_inventory(self):
        return self._init_mean_inventory

    @property
    def init_n_stocks(self):
        return self._init_n_stocks

    @property
    def mean_inventory(self):
        return self._mean_inventory


    def _get_reward(self, action, n_stocks, price):
        try:
             return getattr(self, f'_{action}')(n_stocks, price)
        except Exception:
            raise ValueError('You must pass buy or sell')


    def reset(self):
        self._n_stocks = self._init_n_stocks
        self._mean_inventory = self._init_mean_inventory


    def _buy(self, n_stocks, price):

        reward = self._sell(-n_stocks, price)
        self._update_mean(n_stocks, price)
        return reward if reward != -0 else 0
        


    def _sell(self, n_stocks, price):

        if n_stocks <= self._n_stocks:
            reward = (price - self._mean_inventory) * n_stocks if self._n_stocks else 0
            self._n_stocks -= n_stocks

            return reward 
        return 0

    def _update_mean(self, n_stocks, price):
        frac = n_stocks / self.n_stocks 
        self._mean_inventory = frac * price + (1-frac) * self._mean_inventory



