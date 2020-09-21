

from abc import ABCMeta, abstractmethod
from src.portfolio.state import StatePortfolio
from src.replay.replay_buffer import ReplayBuffer
import numpy as np


class PlayDoubleQlearning(metaclass=ABCMeta):

    def __init__(self, q_eval, env, states_price):

        self._states_env = None
        self._q_eval = q_eval
        self.env = env
        self.shape_env_features = self.q_eval.get_layer('states_env').output_shape[1:]
        self.states_price = states_price


    @property
    def shape_env_features(self):
        return self._shape_env_features

    @property
    def q_eval(self):
        return self._q_eval

    @property
    def states_env(self):
        return self._states_env

    #public methods

    @abstractmethod
    def play(self):
        pass

    def reset(self):
        self.env.reset()
        self.states_env.reset()


    def choose_action(self, current_states, random_probability):
        return self._random_choice() if np.random.random() < random_probability \
            else self._agent_choose_action(current_states)

    # private errors methods

    def _current_state(self):
        return self.states_price[self.env.states_actions.time], self.states_env.values

    def _agent_choose_action(self, current_state):
        state = list(map(lambda state: state[np.newaxis, :], current_state))
        actions = self.q_eval.predict(state)
        return int(np.argmax(actions))


    def _random_choice(self):
        return np.random.choice(self.env.action_spaces)

    def _verify_errors(self, shape):
        self._check_is_array()
        shape = self.states_price.shape
        self._check_number_samples(shape[0])
        self._check_number_delays(shape[1])

    def _play_errors(self, errors):
        if errors == 'verify':
            self._verify_errors()

    def _check_number_samples(self, shape_market_states):
        if not shape_market_states == len(self.env.states_actions.time_series):
            raise ValueError('Mismatch between time series of env and shape of market states')

    def _check_number_delays(self, delays_market_states):
        if not delays_market_states == self.shape_env_features[0]:
            raise ValueError('Mismatch between shape_env_features and market states shape')

    def _check_is_array(self):
        if not isinstance(self.states_price, np.ndarray):
            raise ValueError('You must pass a instance of np.ndarray')




class PlayAndRememberDoubleQlearning:

    def __init__(self, mem_size, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.memory =  ReplayBuffer(mem_size, 
                                    (self.states_price.shape[1:], self.shape_env_features),
                                    len(self.env.action_spaces),
                                    discrete=False)

    def play(self, random_probability, errors='ignore'):

        # check errors
        self._play_errors(errors)
        #reset env and states_env
        self.reset()
        current_state = self._current_state()

        for step in range(len(self.env.states_actions.time_series)):
            #choose action
            action = self.choose_action(current_state, 
                                        random_probability)
            # do action, step and get reward
            reward, next_state_env_tuple = self.env.eval_with_rewards(action)
            #update env states
            self.states_env.update_last(*next_state_env_tuple)
            #remember state_env
            if not self.env.states_actions.terminal:
                next_state = self._current_state()
                self.memory.store_transition(current_state, action, reward, 
                                             next_state, False)
                #update state
                current_state = next_state

class PlayValidationDoubleQlearning():
    
    def play(self, random_probability, errors='ignore'):
        # check errors
        self._play_errors(errors)
        #reset env and states_env
        self.reset()
        current_state = self._current_state()

        for step in range(len(self.env.states_actions.time_series)):
            #choose action
            action = self.choose_action(current_state, 
                                        random_probability)
            # do action, step and get reward
            next_state_env_tuple = self.env.eval_without_rewards(action)
            #update env states
            self.states_env.update_last(*next_state_env_tuple)

            if not self.env.states_actions.terminal:
                #update state
                current_state = self._current_state()

