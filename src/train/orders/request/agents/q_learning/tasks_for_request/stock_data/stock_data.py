from src.train.database.cache.agents.create import CreateAgentTrainCache
from src.train.database.cache.agents.delete import RemoveAgentTrainCache
from src.train.orders.request.agents.q_learning.tasks_for_request.stock_data.get_data import GetDataTask
from src.train.orders.request.agents.q_learning.tasks_for_request.transform_data import TransformData
import pandas as pd
import numpy as np

class StockDataTask:

    def __call__(self, stock_name, data_train_limits, data_validation_limits, delays):

        data_prep = self._data_preparation(stock_name, 
                                           data_train_limits, 
                                           data_validation_limits, 
                                           delays)

        return (*data_prep[-2:], *self._to_cache(data_prep[:-2]))
            

    def _get_features(self, df):
        features = ['weekday', 'dayofyear', 'open', 'high', 'low', 'close', 'volume']
        return df.assign(weekday=df.index.weekday, 
                         dayofyear=df.index.dayofyear).loc[:, features]


    def _data_preparation(self, stock_name, data_train_limits, data_validation_limits, delays):
        
        #get data
        train_data, validation_data = GetDataTask()(stock_name, 
                                                    data_train_limits, data_validation_limits, 
                                                    delays)
        #get_features
        train_features = self._get_features(train_data)
        validation_features = self._get_features(validation_data)
        #embed sequences
        transform_features = TransformData(delays)

        return (*transform_features(train_features), 
                *transform_features(validation_features),
                train_features.index, validation_features.index)


    @staticmethod
    def _limits_to_datetime(limits):
        return tuple(map(pd.to_datetime, limits))


    def _to_cache(self, data_prep_result):
        ids = []
        create_obj = CreateAgentTrainCache()
        for i, _ in enumerate(('train', 'validation')):
            id, _ = create_obj(
                **dict(
                        zip(
                            ('sequences', 'time_values'), 
                            (data_prep_result[2*i],
                             data_prep_result[2*i +1].rename(str).to_dict())
                          )
                      )
            )
                
            ids.append(id)
        return  tuple(ids)

    def remove(self, id_cache):
        return RemoveAgentTrainCache().delete_id(id_cache)