from abc import ABCMeta, abstractmethod
from src.train.database.cache.agents.create import CreateAgentTrainCache
from src.train.database.cache.agents.delete import RemoveAgentTrainCache
import numpy as np

class DataTask(metaclass=ABCMeta):

    _create_agent_cache = CreateAgentTrainCache()
    _remove_cache = RemoveAgentTrainCache()
    
    @property
    @classmethod
    @abstractmethod
    def data_from_db(self):
        pass

    @property
    @classmethod
    @abstractmethod
    def features(self):
        pass

    @abstractmethod
    def _data_preparation(self):
        pass

    def _get_features(self, df):
        df = df.assign(weekday=df.index.weekday, 
                         dayofyear=df.index.dayofyear,
                         )\
            .loc[:, ('weekday', 'dayofyear') + self.features]
        if 'volume' in df.columns:
            return df.assign(volume=np.log1p(df['volume']))
        return df
    def _to_cache(self, data, is_financial=False):
            dict_to_cache = self._not_financial_dict(data) if not is_financial \
                else {'data' : data[0], 
                      'index' : data[1].to_numpy(), 
                      'columns' : data[2].to_numpy()}
            return self._create_agent_cache(**dict_to_cache)[0]
    @staticmethod
    def _not_financial_dict(data):
        return dict(zip(('sequences', 'time_values'), data)) \
            if isinstance(data, (tuple, list)) else {'sequences' : data}

    def remove(self, id_cache):
        return self._remove_cache.delete_id(id_cache)
   