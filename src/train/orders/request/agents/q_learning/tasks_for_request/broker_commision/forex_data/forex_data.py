from src.train.orders.request.agents.q_learning.tasks_for_request.\
    broker_commision.forex_data.get_data import GetDataTask
from src.train.orders.request.agents.q_learning.tasks_for_request.transform_data import TransformData
from src.train.orders.request.agents.q_learning.tasks_for_request.data_task import DataTask

class ForexDataTask(DataTask):

    features = ('close', )
    data_from_db = GetDataTask()

    def __call__(self, from_symbol, to_symbol, index, delays):

        return self._to_cache(
            self._data_preparation(from_symbol, 
                                   to_symbol, 
                                   index, 
                                   delays)
        )
            
    def _data_preparation(self, from_symbol, to_symbol, index, delays):
        #get_features
        features = self._get_features(self.data_from_db(from_symbol, to_symbol, index))
        #embed sequences
        transform_features = TransformData(delays)
        return transform_features(features)
                



