from src.read_database.stock_data import StockDataFromDataBase
import pandas as pd


class GetDataTask:

    _reader = StockDataFromDataBase.dailyadj_dataframe()

    def __call__(self, stock_name, data_train_limits, data_validation_limits, delays):

        init_val, end_val = data_validation_limits
        init_train, end_train = data_train_limits

        return self._data_immediate_validation(stock_name, 
                                               delays, 
                                               init_train, 
                                               end_train, 
                                               end_val) \
            if init_val == 'immediate' else self._data_with_limits(stock_name, 
                                                                   data_train_limits, 
                                                                   data_validation_limits)

    def _data_immediate_validation(self, stock_name, delays, init_train, end_train, end_val):

        init_train, end_train, end_val = self._limits_to_datetime(init_train, end_train, end_val)
        data = self._reader.get(stock_name, init_train, end_val)
        #get train data
        train_data = data.loc[init_train : end_train]
        #get real end train
        end_train = train_data.index[-1]
        val_data = self._get_validation_data_next_day_train_date(data, end_train, delays + 1)
        return train_data, val_data

    def _data_with_limits(self, stock_name, data_train_limits, data_validation_limits):

        #get limits
        init_train_date, end_train_date = self._limits_to_datetime(data_train_limits)
        init_validation_date, end_validation_date = self._limits_to_datetime(data_validation_limits)
        #get data
        train_data = self._reader.get(stock_name, init_train_date, end_train_date)
        val_data = self._reader.get(stock_name, init_validation_date, end_validation_date)

        return train_data, val_data


    def _get_validation_data_next_day_train_date(self, data, end_train, delays):
    
        candidates = data.index <= end_train
        return data.loc[data.index[candidates][-delays]:]

    @staticmethod
    def _limits_to_datetime(*limits):
        return tuple(map(pd.to_datetime, limits))
