import pandas as pd
from src.data_preparation.errors.check_dataframe import CheckSplitDataFrameByGroups
from src.data_preparation.errors.check_datetime_index import CheckDateTimeIndex
from src.data_preparation.datetime_index import DateTimeIndexFeatures
from src.tools.check_components import eval_type_argument
from src.data_preparation.datetime_index import DateTimeIndexFeatures

class SplitDataFrameByGroups:
    
    def __init__(self, format_output=list):
        self.check_errors_bygroups = CheckSplitDataFrameByGroups()
        #get format_output like type instance
        self.__format_output = eval_type_argument(format_output)
        #eval format supported
        self.check_errors_bygroups.check_valid_format_output(self.__format_output)

    def split(self, dataframe, *args, **kwargs):
        groups = dataframe.groupby(*args, **kwargs)
        if self.__format_output == list:
            return [group for by, group in groups]
        return dict(groups.__iter__())

class SplitDateTimeDataFrame(SplitDataFrameByGroups):

    def by_discontinuous_index(self, dataframe, freq_limit):
        return self.split(dataframe=dataframe,
                          by=DateTimeIndexFeatures(dataframe.index).continuos_time_blocks(step=freq_limit))
    
    def by_frecuency(self, dataframe, freq, **kwargs):
        return self.split(dataframe=dataframe, by=pd.Grouper(freq=freq, **kwargs))



        




    
