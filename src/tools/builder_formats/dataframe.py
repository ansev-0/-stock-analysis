import pandas as pd
from numpy import nan


class BuildDataFrameFromDB:


    def build_dataframe_from_timeseries_dict(self,
                                             dataframe,
                                             format_index=None, 
                                             datetime_index=True, 
                                             ascending=None):

        return self._build(True, dataframe, format_index, datetime_index, ascending)


    def build_dataframe_from_financial_timeseries_dict(self,
                                                       dataframe,
                                                       format_index=None, 
                                                       datetime_index=True, 
                                                       ascending=None):

        return self._build(False, dataframe, format_index, datetime_index, ascending)


    def _build(self,
               to_float,
               dataframe,
               format_index=None, 
               datetime_index=True, 
               ascending=None,
               ):

        dataframe = pd.DataFrame.from_dict(dataframe, orient='index')
        dataframe = dataframe.astype(float) if to_float else dataframe
        if datetime_index:
            dataframe.index = pd.to_datetime(dataframe.index, format=format_index)
        if ascending is not None:
            return dataframe.sort_index(ascending=ascending)
        return dataframe
    
