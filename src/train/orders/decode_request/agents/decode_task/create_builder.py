from src.tools.build.dynamic import BuilderWithComponents
from src.train.database.cache.agents.find import FindAgentTrainCache
from src.train.rl_model.commision.dynamic import DynamicCommision
import pandas as pd

class CreateBuilderTask:

    def __call__(self, broker, dict_cache_broker, cache_id):

        builder = BuilderWithComponents()
        builder.register_component('commision', self._create_broker_commision(broker, dict_cache_broker))
        builder.register_component('time_values', self._load_serie_from_cache(cache_id))
        return builder

    def _create_broker_commision(self, broker, dict_cache_broker):
        return DynamicCommision()(broker).from_cache_train(dict_cache_broker)

    def _load_serie_from_cache(self, cache_id):
        return pd.Series(FindAgentTrainCache().\
                find_by_id(cache_id, 
                           projection = {'time_values' : True,
                                         '_id' : False})['time_values'])
