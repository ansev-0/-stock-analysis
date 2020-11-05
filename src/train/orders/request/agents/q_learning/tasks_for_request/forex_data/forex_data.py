from src.train.database.cache.agents.update import UpdateAgentTrainCache
from src.train.orders.request.agents.q_learning.tasks_for_request.forex_data.get_data import GetDataTask
from src.train.orders.request.agents.q_learning.tasks_for_request.transform_data import TransformData
import pandas as pd
import numpy as np


class ForexDataTask:

    def __call__(self, from_symbol, to_symbol, index_train, index_val, delays, cache_ids):

        data_prep = self._data_preparation(from_symbol, to_symbol,
                                           index_train, 
                                           index_val,
                                           delays)

        return self._to_cache(data_prep, cache_ids)
            

    def _get_features(self, df):
        features = ['weekday', 'dayofyear', 'close']
        return df.assign(weekday=df.index.weekday, 
                         dayofyear=df.index.dayofyear).loc[:, features]
    @staticmethod
    def _get_limits_from_index(index):
        return tuple(index[[0,-1]])


    def _data_preparation(self, from_symbol, to_symbol, index_train, index_val, delays):
        
        #get data
        train_data, validation_data = GetDataTask()(from_symbol, to_symbol, 
                                                    index_train, index_val, 
                                                    delays)
        #get_features
        train_features = self._get_features(train_data)
        validation_features = self._get_features(validation_data)
        #embed sequences
        transform_features = TransformData(delays)

        return (
                *transform_features(train_features), 
                *transform_features(validation_features),
                )

     
    def _to_cache(self, data_prep_result, cache_ids):

        update_obj = UpdateAgentTrainCache()
        for i, _ in enumerate(('train', 'validation')):
            update_obj.update_on_id(
                id = cache_ids[i],
                data=dict(
                            zip(
                                ('sequences', 'time_values'), 
                                (data_prep_result[2*i],
                                 data_prep_result[2*i +1].rename(str).to_dict()
                                 )
                               )
                         )
                      )


