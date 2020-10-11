from src.read_database.stock_data import StockDataFromDataBase
from src.data_preparation.tools.expand.embedding import EmbedTimeSeries
from src.train.database.cache.agents.create import CreateAgentTrainCache
from src.train.database.cache.agents.delete import RemoveAgentTrainCache
import pandas as pd
import numpy as np

class StockDataTask:

    _reader = StockDataFromDataBase.dailyadj_dataframe()

    def __call__(self, stock_name, data_train_limits, data_validation_limits, delays):
        return self._to_cache(
            self._data_preparation(stock_name, data_train_limits, data_validation_limits, delays)
        )

    def _get_features(self, df):
        features = ['weekday', 'dayofyear', 'open', 'high', 'low', 'close', 'volume']
        return df.assign(weekday = df.index.weekday, dayofyear = df.index.dayofyear).loc[:, features]


    def _data_preparation(self, stock_name, data_train_limits, data_validation_limits, delays):

        #get limits
        init_train_date, end_train_date = self._limits_to_datetime(data_train_limits)
        init_validation_date, end_validation_date = self._limits_to_datetime(data_validation_limits)
        #get data
        train_dates = self._reader.get(stock_name, init_train_date, end_train_date)
        validation_dates = self._reader.get(stock_name, init_validation_date, end_validation_date)
        #get_features
        train_features = self._get_features(train_dates)
        validation_features = self._get_features(validation_dates)
        #embed sequences
        mbed = EmbedTimeSeries(delays+1)
        train_sequences = np.diff(mbed(train_features[:-1]), axis=1)
        validation_sequences = np.diff(mbed(validation_features[:-1]), axis=1)
        # stock price to use
        close_train_values = train_features.loc[train_features.index[-train_sequences.shape[0]-1:], 'close']
        close_validation_values = validation_features.\
            loc[validation_features.index[-validation_sequences.shape[0]-1:],
                'close']
        return close_train_values, close_validation_values, train_sequences, validation_sequences


    @staticmethod
    def _limits_to_datetime(limits):
        return tuple(map(pd.to_datetime, limits))


    def _to_cache(self, data_prep_result):
        ids = []
        create_obj = CreateAgentTrainCache()
        for i, type_to in enumerate(('train', 'validation')):
            id, _ = create_obj(**dict(
                               zip(('time_values', 'sequences'), 
                                  (data_prep_result[i].tolist(), data_prep_result[i+2])
                                  )
                              )
                      )
            ids.append(id)
        return  tuple(ids)


    def remove(self, id_cache):
        return RemoveAgentTrainCache().delete_id(id_cache)