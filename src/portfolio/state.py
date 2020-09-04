import numpy as np
class StatePortfolio:

    def __init__(self, shape_portfolio):
        self._shape_portfolio = shape_portfolio
        self._values = np.zeros(shape_portfolio)

    @property
    def values(self):
        return self._values

    def update_last(self, *args):
        self._values[0] = np.array(args)
        self._values = np.roll(self.values, -1, axis=0)

    def reset(self):
        self._values = np.zeros(self._shape_portfolio)