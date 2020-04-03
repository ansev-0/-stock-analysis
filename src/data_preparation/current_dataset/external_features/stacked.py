import numpy as np
import pandas as pd
from src.data_preparation.expand.nn_input_output import BuilderIOStacked
from src.data_preparation.scale.minmaxscaler import MinMaxScalerFitTransformMany


class DataSetStackedExternalFeature():

    def __init__(self, serie, samples, steps_delay, feature_range):
        self.__feature_range = feature_range
        self.current_dataset = None
        self.current_dataset_scaled = None
        self.__samples = samples
        self.__steps_delay = steps_delay
        self.__builder_io_stacked = BuilderIOStacked()
        #Get dataframe delays
        dataframe = self.__get_dataframe(serie, steps_delay)
        self.dataset = dataframe.to_numpy()
        #get the index of temporal time of train
        self.dataset_time_index = dataframe.index
        self.__dataset_index = 0


    def update_current_variables(self):
        # get data to use without scaling
        self.current_data = self.__get_current_data()
        #get data scaled
        self.current_scaled_variables = self.__get_current_scaled_variables()
        #add to next step
        self.__dataset_index += 1

    def current_data(self):
        return np.expand_dims(self.current_data, 2)

    def current_data_scaled(self):
        return np.expand_dims(self.current_scaled_variables[1], 2)

    def current_scaler(self):
        return self.current_scaled_variables[0]


    def __get_current_data(self):
        return self.dataset[self.__dataset_index : self.__samples + self.__dataset_index, :]
     
    def __get_current_scaled_variables(self):
        fit_transform_scaler = MinMaxScalerFitTransformMany(self.__feature_range)
        return fit_transform_scaler.array(self.current_data)




    def __get_dataframe(self, serie, sup_limit_range):
        return self.__builder_io_stacked.dataframe_delays_from_serie(serie,
                                                                     (1, sup_limit_range + 1))

