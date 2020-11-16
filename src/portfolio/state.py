import numpy as np

class StatePortfolio:

    def __init__(self, shape_portfolio):
        self._shape_portfolio = shape_portfolio
        self._values = None
        self.reset()

    @property
    def values(self):
        return self._values


    def update_last(self, *args):
        self._values[0] = np.array(args)
        if self._shape_portfolio[0] > 1:
            self._values = np.roll(self.values, -1, axis=0) 

    def reset(self, init_state=None):
        self._values = self._init_state(init_state)

    
    def _init_state(self, init_state):

        if isinstance(init_state, tuple) or isinstance(init_state, list):
            init_tensor = np.zeros(self._shape_portfolio)
            init_tensor[-1] = init_state
            return init_tensor

        elif isinstance(init_state, np.ndarray):
            return init_state

        elif init_state is None:
            return np.zeros(self._shape_portfolio)
        
        raise TypeError('Invalid type of init_state, \
                         You must pass list, tuple or np.ndarray instance')

