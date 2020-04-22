import numpy as np
import pandas as pd
from src.data_preparation.tools.expand.stacked_delay import StackedDataFrameDelay, \
    StackedSerieDelay

class AdapterKerasTimeSeriesStacked:
    
    def __init__(self, range_delays):
        self._range_delays=None
        self.set_range_delays(range_delays)

    @property
    def range_delays(self):
        return self._range_delays

    
    def set_range_delays(self, range_delays):
        self._range_delays = range_delays
        self._builder_from_dataframe = StackedDataFrameDelay(range_delays)
        self._builder_from_serie = StackedSerieDelay(range_delays)

    def list_to_list(self, list_shiftable_pandas):
        return np.split(ary=self._builder_from_dataframe.array_without_nan(
                            self._join_list_shiftable_pandas(list_shiftable_pandas)),
                        indices_or_sections=self._get_index_split(list_shiftable_pandas),
                        axis=2)

    def dict_to_list(self, dict_shiftable_pandas):
        return self.list_to_list(list(dict_shiftable_pandas.values()))

    def dict_to_dict(self, dict_shiftable_pandas):
        return dict(zip(dict_shiftable_pandas.keys(),
                        self.dict_to_list(dict_shiftable_pandas)))

    @staticmethod
    def _get_index_split(list_to_get_index):
        return np.cumsum(tuple(
            map(lambda item: len(item.columns) if isinstance(item, pd.DataFrame) else 1,
                list_to_get_index)))[:-1]

    @staticmethod
    def _join_list_shiftable_pandas(list_to_join):
        return pd.concat(list_to_join, axis=1, join='inner', sort=False)


    