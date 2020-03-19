import pandas as pd
from src.data_preparation.errors.check_split_time_dataframe import CheckSplitDataFrameByGroups
from src.data_preparation.errors.check_split_time_dataframe import CheckSplitDataFrame
from src.tools.check_components import eval_type_argument

class SplitDataFrameByGroups:
    def __init__(self, format_output=list):

        self.check_errors_bygroups = CheckSplitDataFrameByGroups()
        #get format_output like type instance
        self.__format_output = eval_type_argument(format_output)
        #eval format supported
        self.check_errors_bygroups.check_valid_format_output(self.__format_output)

    def split(self, dataframe, *args, **kwards):
        groups = dataframe.groupby(*args, **kwards)

        if self.__format_output == list:
            return [group for by, group in groups]
        return dict(groups.__iter__())

class SplitDateTimeDataFrame(SplitDataFrameByGroups):

    def __init__(self, **kwards):
        self.check_errors = CheckSplitDataFrame()
        super().__init__(**kwards)

    def by_discontinuous_index(self, dataframe, freq_limit):
        #Check DateTimeIndex
        self.check_errors.check_datetime_index(index=dataframe.index)
        #Take blocks to use split function
        continuos_time_blocks = self.__get_blocks_continuous_periods(dataframe, freq_limit)
        #Get output
        return self.split(dataframe=dataframe, by=continuos_time_blocks)
    
    def by_frecuency(self, dataframe, freq, **kwards):
        return self.split(dataframe=dataframe, by=pd.Grouper(freq=freq, **kwards))

    def __get_blocks_continuous_periods(self, dataframe, freq):
        return dataframe.index.to_series().diff().ge(pd.Timedelta(freq)).cumsum()



        




    
