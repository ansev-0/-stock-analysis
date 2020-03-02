import pandas as pd
def build_dataframe_from_timeseries_dict(dataframe, format_output=None, datetime_index=True, ascending=None):
    dataframe=pd.DataFrame.from_dict(dataframe, orient='index').astype(float)
    if datetime_index:
        dataframe.index = pd.to_datetime(dataframe.index, format= format_output)
    if ascending is not None:
        return dataframe.sort_index(ascending=ascending)
    return dataframe
    
