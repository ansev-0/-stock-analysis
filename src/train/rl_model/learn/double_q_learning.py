import numpy as np
from abc import ABCMeta, abstractproperty

class LearnDoubleQlearning:
    
    @abstractproperty
    def q_eval(self):
        pass

    @abstractproperty
    def gamma(self):
        pass

    @abstractproperty
    def q_target(self):
        pass

    def learn_and_update_q_target(self, memory, *args, **kwargs):
        fit = self.learn(memory, *args, **kwargs)
        self.update_q_target()
        return fit

    def learn_and_update_q_target_from_discrete_actions(self, memory, *args, **kwargs):
        memory[1] = self._get_indices_from_discrete_actions(memory[1])
        return self.learn_and_update_q_target(memory, *args, **kwargs)

    def learn_from_discrete_actions(self, memory, *args, **kwargs):
        memory[1] = self._get_indices_from_discrete_actions(memory[1])
        return self.learn(memory, *args, **kwargs)

    def learn(self, memory, *args, **kwargs):
        #unpack
        states, actions, rewards, new_states, terminal_signals = memory
        #get predictions
        q_next = self.q_target.predict(new_states)
        q_eval = self.q_eval.predict(new_states)
        q_pred = self.q_eval.predict(states)
        q_target = q_pred
        #get target
        max_actions = np.argmax(q_eval, axis=1).astype(int)
        batch_index = range(states[0].shape[0])
        # fit q_eval
        q_target[batch_index, actions] = rewards + terminal_signals * self.gamma * q_next[batch_index, max_actions]
        fit = self.q_eval.fit(states, q_target, *args, **kwargs)
        
        return fit

    def update_q_target(self):
        self.q_target.set_weights(self.q_eval.get_weights())
        


    def _get_indices_from_discrete_actions(self, actions):
        return np.dot(actions, np.arange(actions.shape[1], dtype=np.int8))
