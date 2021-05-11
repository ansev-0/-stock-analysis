from src.train.orders.request.agents.q_learning.tasks_for_request.data_task import DataTask
from src.train.orders.request.agents.q_learning.tasks_for_request.stock_data.get_data import GetDataTask
from src.train.orders.request.agents.q_learning.tasks_for_request.transform_data import TransformData
from pandas import to_datetime

class StockDataTask(DataTask):

    features = ('open', 'high', 'low', 'close', 'volume')
    data_from_db = GetDataTask()

    def __call__(self, stock_name, data_train_limits, data_validation_limits, delays):

        data_prep = self._data_preparation(stock_name, 
                                           data_train_limits, 
                                           data_validation_limits, 
                                           delays)

        return (*data_prep[2:], *tuple(self._to_cache(data) for data in data_prep[:2]))
            

    def _data_preparation(self, stock_name, data_train_limits, data_validation_limits, delays):
        
        #get data
        train_data, validation_data = self.data_from_db(stock_name, 
                                                        data_train_limits, 
                                                        data_validation_limits, 
                                                        delays)
        #get_features
        train_features = self._get_features(train_data)
        validation_features = self._get_features(validation_data)
        #embed sequences
        transform_features = TransformData(delays)
        train_, validation_ = transform_features(train_features), transform_features(validation_features)
        print('First incr : ', train_[0][0, [-3, -2, -1], -2])
        print(list(train_[1])[:1])

        return train_, validation_,\
            train_[0].shape[0], validation_[0].shape[0],\
            train_features.index, validation_features.index


    @staticmethod
    def _limits_to_datetime(limits):
        return tuple(map(to_datetime, limits))

