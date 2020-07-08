class ResampleOhlcDataFrame:

    _ohlcv_dict = {'open' : 'first',
                  'high' : 'max',
                  'low' : 'min',
                  'close' : 'last',
                  'volume' : lambda x: x.sum(min_count=1)}

    def __init__(self, freq):
        self.freq=freq

    @property
    def ohlcv_dict(self):
        return self._ohlcv_dict

    def resample(self, dataframe, add_cols=None):

        if not add_cols:
            agg_dict = self.ohlcv_dict
        else:
            add_cols_dict = self._get_add_cols_dict(dataframe.columns, add_cols)
            agg_dict = self._join_add_cols_dict(add_cols_dict)

        return self._get_agg_dataframe(dataframe, agg_dict)

    def _get_agg_dataframe(self, dataframe, dict_to_agg):
        return dataframe.resample(self.freq).agg(dict_to_agg)

    def _get_add_cols_dict(self, columns, add_cols):

        if isinstance(add_cols, dict):
            return add_cols
        add_cols_names = self._get_add_cols_names(columns)
        return self._add_cols_dict_from_other(add_cols_names, add_cols)

    def _join_add_cols_dict(self, add_cols_dict):
        return dict(self._ohlcv_dict, **add_cols_dict)


    @staticmethod
    def _add_cols_dict_from_other(add_cols_names, add_cols):
        return dict(zip(add_cols_names, [add_cols] * len(add_cols_names)))


    @staticmethod
    def _get_add_cols_names(columns):
        return columns.difference(['open', 'close', 'high', 'low', 'volume'])


