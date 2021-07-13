import numpy as np
from numpy.random import default_rng


class BufferStates(dict):

    '''
    This class is used to simplify the update of the states when there is more than one numpy.
    Array to update (market states and portfolio states).
    '''

    def __init__(self, input_shapes, mem_size, names_states=None):

        self._input_shapes = input_shapes
        self._mem_size = mem_size
        self._names_states = names_states


        if names_states is None:
            self._names_states = range(len(input_shapes))

        elif len(names_states == len(input_shapes)):
            self._names_states = names_states

        else:
            raise ValueError('length of input_shapes must be equal to length of names_states')

        for i, shape in zip(self._names_states, self._input_shapes):
                self[i] = np.zeros((mem_size, *shape)) #initialize states

    def update_pos(self, index_pos, arrays, names_to_update=None):

        '''
        Update the arrays corresponding to the keys passed (names_to_update),
        if the keys are not specified, 
        the number of arrays must be equal to the total number of shapes specified when creating the object.

        '''
        if names_to_update is None:
            names_to_update = self._names_states

        for key, value in zip(names_to_update, arrays):
            self[key][index_pos] = value


    def get_pos(self, index_pos, names_filter=None, return_dict=False):

        '''
        Returns the position of the specified index.
        '''

        if names_filter is None:
            names_filter = self._names_states

        return {key : self[key][index_pos] for key in names_filter} \
            if return_dict else list(map(lambda key: self[key][index_pos], names_filter))

class ReplayBuffer:

    '''
    Save training states to enable the learning phase.
    '''

    def __init__(self, mem_size, input_shapes, n_actions=None, discrete=False, names_states=None):

        self._rng = default_rng()
        self.mem_size = mem_size #longitud maxima de la memoria
        self.mem_ctr = 0 ## contador para la memoria
        self._save_action_function = None
        self.discrete = discrete
        
        #fields of memory
        #states
        self.state_memory = BufferStates(input_shapes, self.mem_size, names_states)
        self.new_state_memory = BufferStates(input_shapes, self.mem_size, names_states)
        #actions 
        self._set_action_memory(n_actions)
        #reward
        self.reward_memory = np.zeros(self.mem_size)
        #terminal
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.float32)


    @property
    def discrete(self):
        return self._discrete

    @discrete.setter
    def discrete(self, discrete):
        self._discrete = discrete
        self._update_save_action_function()

    def store_transition(self, state, action, reward, new_state, done):

        #save states
        self.state_memory.update_pos(self.mem_ctr, state)
        self.new_state_memory.update_pos(self.mem_ctr, new_state)
        #save actions
        self.action_memory[self.mem_ctr] = self._save_action_function(action)
        ## save reward
        self.reward_memory[self.mem_ctr] = reward
        ## save done
        self.terminal_memory[self.mem_ctr] = 1-int(done)
        #incr counter
        self.mem_ctr += 1

        self.mem_ctr %= self.mem_size

    def sample_buffer(self, batch_size, sort=False, replace=True):

        max_mem = self.mem_ctr if self.mem_ctr > 0 else self.mem_size
        batch = self._rng.choice(max_mem, size=batch_size if batch_size < max_mem else max_mem, replace=replace)

        if sort:
            batch = list(sorted(batch))

        states = self.state_memory.get_pos(batch)
        new_states = self.new_state_memory.get_pos(batch)
        actions = self.action_memory[batch]
        rewards = self.reward_memory[batch]
        terminal = self.terminal_memory[batch]

        return states, actions, rewards, new_states, terminal


    def _update_save_action_function(self):
        self._save_action_function = self._discrete_save_action_function \
            if self.discrete else lambda action: action

    def _discrete_save_action_function(self, action):
        actions = np.zeros(self.action_memory.shape[1], dtype=np.int8)
        actions[action] = 1
        return actions


    def _set_action_memory(self, n_actions):
        if self.discrete:
            self.action_memory = np.zeros((self.mem_size, n_actions), 
                                          dtype=np.int8) 
        else:
            self.action_memory = np.zeros((self.mem_size,), dtype=np.int8)
 