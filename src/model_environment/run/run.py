from src.model_environment.actions.save_time_actions import TimeActions
from abc import ABCMeta, abstractmethod

class RunEnv(metaclass = ABCMeta):

    def __init__(self, states_actions, reward_action_done=None, reward_action_not_done=None):

        self.indexes_actions = TimeActions()
        self.reward_action_done = reward_action_done
        self.reward_action_not_done = reward_action_not_done
        self.states_actions = states_actions

    @abstractmethod
    def transition(self):
        pass

    @abstractmethod
    def transition_with_rewards(self):
        pass

    def reset(self):
        self.states_actions.reset()
        self.indexes_actions.reset()
        if self.reward_action_done is not None:
            self.reward_action_done.reset() 
        if self.reward_action_done is not None:
            self.reward_action_not_done.reset()


class RunQlearningEnv(RunEnv):



    def transition(self, action, n_stocks=None, frac=None):
        
        _,_, action_done, income = self.states_actions.do_action(action, n_stocks, frac)
        self.indexes_actions.save(action, self.states_actions.time, action_done, n_stocks, frac)
        

        if not self.states_actions.terminal:
            self.states_actions.step()

        profit = self.states_actions.profit


        return profit, income, self.states_actions.max_purchases(),\
             self.states_actions.max_sales()

    def transition_with_rewards(self, action, n_stocks=None, frac=None):

        real_frac, real_n_stocks, action_done, income = self.states_actions.do_action(action, n_stocks, frac)
        self.indexes_actions.save(action, self.states_actions.time, action_done, n_stocks, frac)

        price = self.states_actions.stock_price
        profit = self.states_actions.profit
        time = self.states_actions.time

        if action_done:
            rewards = self.reward_action_done.reward(profit = profit, 
                                                     action=action, time=time, 
                                                     n_stocks=real_n_stocks, 
                                                     price = price,
                                                     frac=real_frac)   
        else:
            rewards = self.reward_action_not_done.reward(profit = profit, 
                                                         action=action, time=time,
                                                         price = price)

        if not self.states_actions.terminal:
            self.states_actions.step()

        profit = self.states_actions.profit

        return rewards, profit, income, self.states_actions.max_purchases(), \
            self.states_actions.max_sales()



    @staticmethod
    def _check_valid_action(action):
        if action not in ('buy', 'sell', 'no_action'):
            raise ValueError('You must pass buy, sell or no_action')


class OutputModelActionAdapter:
    _keys = ('action', 'n_stocks', 'frac')
    def __init__(self, unit_actions=('buy', 'sell', 'no_action')):

        self.adapters = {i : dict(zip(self._keys, 
                                  (val, 1, None))) 
                         for i, val in enumerate(unit_actions)}

    def add_fracs(self, buy_fracs, sell_fracs):

        self._add_fracs('buy', buy_fracs)
        self._add_fracs('sell', buy_fracs)
        return self.adapters

    def _add_fracs(self, action, fracs):

        self.adapters.update({i : dict(zip(self._keys,
                                           (action, None, frac)))
        for i, frac in enumerate(fracs, len(self.adapters))})


class RunEnvAdaptModel(RunQlearningEnv):

    def __init__(self, adapter, *args, **kwargs):
        self.adapter = adapter
        super().__init__(*args, **kwargs)

    def eval_with_rewards(self, action):
        return self.transition_with_rewards(**self.adapter[action])

    def eval_without_rewards(self, action):
        return self.transition(**self.adapter[action])


        
#adapter = OutputModelActionAdapter()
#fracs = adapter.add_fracs((0.25, 0.5, 0.75), (0.25, 0.5, 0.75))
#pass

