import pandas as pd
import numpy as np
from src.tools.pandas_tools import remove_enumerate_axis, columns_to_datetime
from src.tools.mappers import map_dict_from_underscore, switch_None


class FormatBuilderAlphavantage:

    def __init__(self):
        self._to_frame = BuildDataFrame()
        self._map_builder = {'TIME': {'FRAME': self._to_frame.time_series,
                                      'DICT_DATA': lambda json: json[list(json)[1]]},
                             'GLOBAL': {'FRAME': self._to_frame.stock_time_series_symbol,
                                        'DICT_DATA': lambda json: json},
                             'SYMBOL': {'FRAME': self._to_frame.stock_time_series_symbol,
                                        'DICT_DATA': lambda json: json['bestMatches']},
                             'CURRENCY': {'FRAME': self._to_frame.cryptocurrencis,
                                          'DICT_DATA': lambda json: json},
                             'FX': {'FRAME': self._to_frame.time_series,
                                    'DICT_DATA': lambda json: json[list(json)[1]]},
                             'DIGITAL': {'FRAME': self._to_frame.time_series,
                                         'DICT_DATA': lambda json: json[list(json)[1]]},
                             'SECTOR': {'FRAME': self._to_frame.sector_performance,
                                        'DICT_DATA': lambda json:
                                                     dict(filter(lambda x: x[0] != 'Meta Data',
                                                                 json.items()))}                  
                            }

    def build_frame(self, json, function, decoded_function=None, **kwards):
        map_function = switch_None(decoded_function, function)
        functions = map_dict_from_underscore(dict_to_map=self._map_builder,
                                             function=map_function,
                                             n=0,
                                             default_key='TIME')
        return functions['FRAME'](data=functions['DICT_DATA'](json), **kwards)

    def get_data_dict(self, json, function, decoded_function=None):
        map_function = switch_None(decoded_function, function)
        return map_dict_from_underscore(dict_to_map=self._map_builder,
                                        function=map_function,
                                        n=0,
                                        default_key='TIME')['DICT_DATA'](json)


class BuildDataFrame:

    def time_series(self,
                    data,
                    to_datetime=True,
                    format_datetime=None,
                    ascending=True,
                    datatype=float,
                    enumerate_axis=False
                    ):
        dataframe = pd.DataFrame.from_dict(data, orient='index').astype(datatype)
        if not enumerate_axis:
            dataframe.columns = remove_enumerate_axis(dataframe.columns)
        if to_datetime:
            dataframe.index = pd.to_datetime(dataframe.index, format=format_datetime)
            dataframe = dataframe.sort_index(ascending=ascending)
        return dataframe

    def stock_time_series_symbol(self,
                                 data,
                                 to_timedelta=[True, True],
                                 enumerate_axis=False,
                                 symbol_index=True,
                                 formats=None
                                 ):
        dataframe = pd.DataFrame(data)
        if symbol_index:
            dataframe = dataframe.set_index('1. symbol')

        cols_time = ['5. marketOpen', '6. marketClose']
        if np.array(to_timedelta).any():
            dataframe[cols_time] = columns_to_datetime(dataframe=dataframe[cols_time],
                                                       formats=formats,
                                                       convert=to_timedelta)
        if not enumerate_axis:
            dataframe.columns = remove_enumerate_axis(dataframe.columns)
        return dataframe

    def stock_time_series_global(self,
                                 data,
                                 include_symbol=True,
                                 enumerate_axis=False,
                                 to_datetime=True,
                                 orient='columns'
                                 ):
        if not include_symbol:
            data['Global Quote'] = dict(filter(lambda x: x[0] != '01. symbol',
                                               data['Global Quote'].items()))
        return self._dataframe_1d(data=data,
                                  to_datetime=to_datetime,
                                  enumerate_axis=enumerate_axis,
                                  orient=orient,
                                  cell_datetime=['07. latest trading day', 'Global Quote'])

    def cryptocurrencis(self, data, orient='columns', to_datetime=True, enumerate_axis=False):
        #This function could be directly introduced in self._map_builder['SECTOR']['FRAME']
        #It has been created to add functionalitiesin the future
        return self._dataframe_1d(data=data,
                                  to_datetime=to_datetime,
                                  enumerate_axis=enumerate_axis,
                                  orient=orient,
                                  cell_datetime=['6. Last Refreshed',
                                                 'Realtime Currency Exchange Rate'])

    def sector_performance(self, data):
        #This function could be directly introduced in self._map_builder['SECTOR']['FRAME']
        #It has been created to add functionalitiesin the future.
        return pd.DataFrame(data)


    def _dataframe_1d(self, data, cell_datetime, to_datetime, enumerate_axis, orient):

        dataframe = pd.DataFrame(data)
        if to_datetime:
            dataframe.loc[cell_datetime[0],
                          cell_datetime[1]] = pd.to_datetime(dataframe.loc[cell_datetime[0],
                                                                           cell_datetime[1]])
        if not enumerate_axis:
            dataframe.index = remove_enumerate_axis(dataframe.index)

        if orient == 'index':
            dataframe = dataframe.T
        return dataframe
