import pandas as pd
def build_dataframe_from_timeseries_dict(dataframe,
                                         format_index=None, datetime_index=True, ascending=None):
    dataframe = pd.DataFrame.from_dict(dataframe, orient='index').astype(float)
    if datetime_index:
        dataframe.index = pd.to_datetime(dataframe.index, format=format_index)
    if ascending is not None:
        return dataframe.sort_index(ascending=ascending)
    return dataframe
    
