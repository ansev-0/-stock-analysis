from abc import ABCMeta, abstractmethod

class RunEnv(metaclass = ABCMeta):

    def __init__(self, 
                 states_actions, 
                 reward_action_done=None, 
                 reward_action_not_done=None):

        
        self.reward_action_done = reward_action_done
        self.reward_action_not_done = reward_action_not_done
        self.states_actions = states_actions

    @abstractmethod
    def transition(self):
        pass

    @abstractmethod
    def transition_with_rewards(self):
        pass
    
    @abstractmethod
    def reset(self):
        pass


class OutputModelActionAdapter:

    _keys = ('action', 'n_stocks', 'frac')

    def __init__(self, load_default=True):
        self._adapter = self._load_default_actions() if load_default else {}


    def __call__(self):
        return self._adapter

    def add_fracs(self, buy_fracs, sell_fracs):
        self._add_fracs('buy', buy_fracs)
        self._add_fracs('sell', buy_fracs)


    def add_n_stocks(self, buy_n_stocks, sell_n_stocks):
        self._add_fracs('buy', buy_n_stocks)
        self._add_fracs('sell', sell_n_stocks)


    def _add_fracs(self, action, fracs):
        self._adapter.update({i : dict(zip(self._keys,
                                           (action, None, frac)))
        for i, frac in enumerate(fracs, len(self._adapter))})

    def _add_amount(self, action, n_stocks):
        self._adapter.update({i : dict(zip(self._keys,
                                           (action, n_stock, None)))
        for i, n_stock in enumerate(n_stocks, len(self._adapter))})

    def _load_default_actions(self):
        return {i : dict(
                            zip(self._keys, 
                                      (val, 
                                       1 if val != 'no_action' else 0,
                                       None)
                                    )
                            ) 
                for i, val in enumerate(('buy', 'sell', 'no_action'))}
        

