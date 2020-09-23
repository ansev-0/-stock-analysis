
from matplotlib import pyplot as plt
import numpy as np
from src.tools.colors import ColorsIntensistyRGB

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
        plt.grid()
        plt.plot(self.serie)
        self._fig.canvas.draw_idle()
        plt.pause(0.5)
        
        


    def update_figure(self, args_tuple, kwargs_tuple):

        if len(self._ax.lines) > 1:
            self._remove_marks()


        self._draw_marks(args_tuple, kwargs_tuple)
        
    def _draw_marks(self, args_tuple, kwargs_tuple):
        for args, kwargs in zip(args_tuple, kwargs_tuple):
            self._ax.plot(self.serie, *args, **kwargs)
            self._fig.canvas.draw_idle()
        plt.pause(0.01)
        self._ax.legend()
        plt.pause(0.01)
    
    def _remove_marks(self):

        for i in range(len(self._ax.lines)-1):
            lines= self._ax.lines.pop(1)
        plt.pause(0.01)

class ShowSellBuyOPerations(ShowOperations):

    colors = ColorsIntensistyRGB(0.25)


    def update(self, indexes_buy, indexes_sell):
        self.update_figure(
                           (('^'), ('v')), 
                           ({'label' : 'Buy', 'markevery' : indexes_buy, 'markersize': 5, 'color' : 'r'}, 
                            {'label' : 'Sell','markevery' : indexes_sell, 'markersize': 5, 'color' : 'g'})
                          )
    
    def update_percentages(self, dict_indexes):

        counters, dict_filtered = self._split_and_filter_indexes_keys(dict_indexes)
        colors = self.colors.get_colors(*counters)
        args = self._get_args(counters)
        kwargs = self._get_kwargs(colors, dict_filtered)
        self.update_figure(args, kwargs)

    @staticmethod
    def _get_kwargs(colors, dict_filtered):
        return tuple({'label' : item[0], 
                      'markevery' : item[1], 
                      'markersize' : 5, 
                      'color' : color}
                      for color, item in zip(colors, dict_filtered.items()))
            

    @staticmethod
    def _get_args(counters):
        return tuple(np.repeat(np.array(('^',  'o', 'v')), counters))

    @staticmethod
    def _split_and_filter_indexes_keys(dict_indexes):
        counters = [0, 0, 0]
        buy_dict, sell_dict, no_actions_dict = {}, {}, {}

        for key, value in dict_indexes.items():

            if 'buy' in key and  not 'pred' in key:
                counters[0]+=1
                buy_dict[key] = value
            elif 'sell' in key and  not 'pred' in key:
                counters[2]+=1
                sell_dict[key] = value
            elif 'no_action' in key:
                counters[1]+=1
                no_actions_dict[key] = value

        return counters, dict(buy_dict,  **no_actions_dict, **sell_dict)





    
