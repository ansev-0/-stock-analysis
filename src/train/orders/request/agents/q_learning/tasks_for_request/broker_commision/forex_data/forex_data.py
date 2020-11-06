from src.train.orders.request.agents.q_learning.tasks_for_request.\
    broker_commision.forex_data.get_data import GetDataTask
from src.train.orders.request.agents.q_learning.tasks_for_request.transform_data import TransformData
from src.train.orders.request.agents.q_learning.tasks_for_request.data_task import DataTask

class ForexDataTask(DataTask):

    features = ('close', )
    data_from_db = GetDataTask()
    def __call__(self, from_symbol, to_symbol, index_train, index_val, delays):

        data_prep = self._data_preparation(from_symbol, to_symbol,
                                           index_train, 
                                           index_val,
                                           delays)

        return self._to_cache(data_prep)
            

    def _data_preparation(self, from_symbol, to_symbol, index_train, index_val, delays):
        
        #get data
        train_data, validation_data = self.data_from_db(from_symbol, to_symbol, 
                                                        index_train, index_val, 
                                                        )
        #get_features
        train_features = self._get_features(train_data)
        validation_features = self._get_features(validation_data)
        #embed sequences
        transform_features = TransformData(delays)

        return transform_features(train_features), transform_features(validation_features)
                

    @staticmethod
    def _get_limits_from_index(index):
        return tuple(index[[0,-1]])




