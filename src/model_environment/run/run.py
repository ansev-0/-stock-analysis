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




