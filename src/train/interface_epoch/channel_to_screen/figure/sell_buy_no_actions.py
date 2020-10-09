from src.view.train.show_operations import ShowSellBuyOPerations
from src.train.database.cache.agents.find import FindAgentTrainCache
import pandas as pd

class SellBuyNoActionsOPerationsFigure:

    def __init__(self, id_cache):
        self._show_obj = ShowSellBuyOPerations(self._get_serie(id_cache))

    def __call__(self, epoch, env):

        if epoch == 1:
            self._show_obj.initialize()
        self._show_obj.update_percentages(env.indexes_actions.timeactions)


    @staticmethod
    def _get_serie(id_cache):
        return pd.Series(FindAgentTrainCache().\
                find_by_id(id_cache, 
                           projection = {'time_values' : True,
                                         '_id' : False})['time_values'])[:-1]
