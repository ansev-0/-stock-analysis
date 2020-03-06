import pandas as pd
from src.data_preparation.errors.check_time_series_dataframe import CheckSplitDataFrame
from src.tools.check_components import eval_type_argument

class SplitDataFrame:

    def __init__(self, format_output=list):

        self.check_errors = CheckSplitDataFrame()
        #get format_output like type instance
        self.__format_output = eval_type_argument(format_output)
        #eval format supported
        self.check_errors.check_valid_format_output(self.__format_output)

    def by_discontinuous_index(self, dataframe, freq_limit):
        #Check DateTimeIndex
        self.check_errors.check_datetime_index(index=dataframe.index)
        #Take blocks to use pandas.DataFrame.GroupBy
        continuos_time_blocks = self.__get_blocks_continuous_periods(dataframe, freq_limit)
        #Get output
        return self.__split_groupby(dataframe=dataframe, by=continuos_time_blocks)
    
    def by_frecuency(self, dataframe, freq, **kwards):
        return self.__split_groupby(dataframe=dataframe, by=pd.Grouper(freq=freq, **kwards))

    def __get_blocks_continuous_periods(self, dataframe, freq):
        return dataframe.index.to_series().diff().ge(pd.Timedelta(freq)).cumsum()

    def __split_groupby(self, dataframe, by, **kwards):
        groups = dataframe.groupby(by=by, **kwards)

        if self.__format_output == list:
            return [group for by, group in groups]
        else:
            return dict(groups.__iter__())

        




    
