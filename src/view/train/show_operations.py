
from matplotlib import pyplot as plt
import numpy as np

class ShowOperations:

    def __init__(self, serie, n_operations):
        self.serie = serie
        self.n_operations = n_operations
        self._fig = None
        self._ax = None

    @property
    def fig(self):
        return self._fig

    @property
    def ax(self):
        return self._ax

    def initialize(self, *args, **kwargs):
        self._fig, self._ax = plt.subplots(*args, **kwargs)
        plt.ion()
        plt.show()
        plt.plot(self.serie)
        self._fig.canvas.draw_idle()
        plt.pause(1)


    def update_figure(self, args_tuple, kwargs_tuple):

        if len(self._ax.lines) > 1:
            self._remove_marks()
        self._draw_marks(args_tuple, kwargs_tuple)
        

    def _draw_marks(self, args_tuple, kwargs_tuple):
        for args, kwargs in zip(args_tuple, kwargs_tuple):
            self._ax.plot(self.serie, *args, **kwargs)
            self._fig.canvas.draw_idle()
            plt.pause(0.001)


    def _remove_marks(self):
        for i in range(self.n_operations):
            _ = self._ax.lines.pop(1)
            #line.remove()


class ShowSellBuyOPerations(ShowOperations):
    def update(self, indexes_buy, indexes_sell):
        self.update_figure((('^'), ('v')), ({'label' : 'Buy', 'markevery' : indexes_buy, 'markersize': 5, 'color' : 'r'}, 
                                            {'label' : 'Sell','markevery' : indexes_sell, 'markersize': 5, 'color' : 'g'}))
    
