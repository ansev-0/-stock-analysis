from abc import ABCMeta, abstractmethod
from src.train.database.cache.agents.create import CreateAgentTrainCache
from src.train.database.cache.agents.delete import RemoveAgentTrainCache

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
        return df.assign(weekday=df.index.weekday, 
                         dayofyear=df.index.dayofyear)\
            .loc[:, ('weekday', 'dayofyear') + self.features]

    def _to_cache(self, data_prep_result):
        ids = []

        for i, _ in enumerate(('train', 'validation')):
            id, _ = self._create_agent_cache(
                **dict(
                        zip(
                            ('sequences', 'time_values'), 
                            data_prep_result[i]
                            )
                        )
            )  
            ids.append(id)

        return  tuple(ids)

    def remove(self, id_cache):
        return self._remove_cache.delete_id(id_cache)
   