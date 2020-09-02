import numpy as np



class States(dict):

    def __init__(self, input_shapes, mem_size, names_states=None):

        self._mem_size = mem_size
        self._names_states = names_states
        self._input_shapes = input_shapes

        if names_states is None:
            self._names_states = range(len(input_shapes))

        elif len(names_states == len(input_shapes)):
            self._names_states = names_states

        else:
            raise ValueError('length of input_shapes must be equal to length of names_states')

        for i, shape in zip(self._names_states, self._input_shapes):
                self[i] = np.zeros((mem_size, *shape))

    def update_pos(self, index_pos, arrays, names_to_update=None):

        if names_to_update is None:
            names_to_update = self._names_states

        for key, value in zip(names_to_update, arrays):
            self[key][index_pos] = value


    def get_pos(self, index_pos, names_filter=None):

        if names_filter is None:
            names_filter = self._names_states

        return {key : self[key][index_pos] for key in names_filter}





class ReplayBuffer:

    def __init__(self, mem_size, input_shapes, n_actions, discrete=False, names_states=None):

        self.mem_size = mem_size #longitud maxima de la memoria
        self.mem_ctr = 0 ## contador para la memoria
        self._save_action_function = None
        self.discrete = discrete
        
        #fields of memory
        #states
        self.state_memory = States(input_shapes, self.mem_size, names_states)
        self.new_state_memory = States(input_shapes, self.mem_size, names_states)
        #actions 
        self.action_memory = np.zeros((self.mem_size, n_actions), dtype=np.int8)
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
        #get index of pos memory to fill
        index = self.mem_ctr % self.mem_size
        #save states
        self.state_memory.update_pos(index, state)
        self.new_state_memory.update_pos(index, new_state)
        #save actions
        self.action_memory[index] = self._save_action_function(action)
        ## save reward
        self.reward_memory[index] = reward
        ## save done
        self.terminal_memory[index] = 1-int(done)
        #incr counter
        self.mem_ctr += 1

    def sample_buffer(self, batch_size, sort=False):

        max_mem = min(self.mem_ctr, self.mem_size)
        batch = np.random.choice(max_mem, batch_size)

        if sort:
            batch = list(sorted(batch))

        states = self.state_memory.get_pos(batch)
        new_states = self.new_state_memory.get_pos(batch)

        actions = self.action_memory[batch]
        rewards = self.reward_memory[batch]
        terminal = self.terminal_memory[batch]

        return states, actions, rewards, new_states, terminal


    def _update_save_action_function(self):
        self._save_action_function = self._discrete_save_action_function if self.discrete else lambda action: action

    def _discrete_save_action_function(self, action):
        actions = np.zeros(self.action_memory.shape[1], dtype=np.int8)
        actions[action] = 1
        return actions

