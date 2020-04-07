import numpy as np
import pandas as pd
class SplitIO:

    def __init__(self, output_delays):
        self.output_delays = output_delays
    #instance public methods
    def dict_from_frame(self, dataframe, keys=None):
        return self.__create_dict_from_frame(dataframe,
                                             lambda frame: frame,
                                             self.output_delays,
                                             keys)

    def dict_array_from_frame(self, dataframe, keys=None):
        return self.__create_dict_from_frame(dataframe,
                                             lambda frame: frame.to_numpy(),
                                             self.output_delays,
                                             keys)

    def dict_array_from_array(self, array, keys=None):
        return dict(zip(self.__get_valid_keys(keys), self.tuple_array_from_array))                                                 

    def tuple_from_frame(self, dataframe):
        return self.__create_tuple_from_frame(dataframe, lambda frame: frame)
        
    def tuple_array_from_frame(self, dataframe):
        return self.__create_tuple_from_frame(dataframe, lambda frame: frame.to_numpy())

    def tuple_array_from_array(self, array, keys=None):
        return array[:, :-self.output_delays], array[:, -self.output_delays:]

    # instance private methods
    def __create_tuple_from_frame(self, dataframe, transform_function):
        return tuple(transform_function(group) 
                     for _, group in self.groups(dataframe, lambda arr: arr))
    
    def __create_dict_from_frame(self, dataframe, transform_function, keys):
        return {by : transform_function(group)
                for by, group in self.__groups(dataframe,
                                               lambda arr: np.where(arr, *self.__get_valid_keys(keys)))}

    def __groups(self, dataframe, function_by):
        return dataframe.groupby(by=function_by(self.__get_by_array(dataframe)),
                                 axis=1)

    def __get_by_array(self, dataframe):
        return np.arange(len(dataframe.columns)) < self.output_delays
    
    #statics privates methods
    @staticmethod
    def __get_valid_keys(keys_user):
        if not keys_user:
            return ('x','y')

    
