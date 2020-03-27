import numpy as np
import pandas as pd
from src.data_preparation.nn_input_output import BuilderIOStacked


class CurrentDataSetAddFeatures():

    def __init__(self, dataframe, batch_size, steps_delay):
        self.current_dataset = None
        self.current_dataset_scaled = None
        self.__batch_size = batch_size
        self.__steps_delay = steps_delay
        self.__n_features = len(dataframe.columns)
        self.__builder_io_stacked = BuilderIOStacked()
        dataframe = pd.concat([self.__get_dataframe(serie, steps_delay)
                               for _, serie in dataframe.items()],
                              axis=1)
        self.dataset = dataframe.to_numpy()
        self.dataset_time_index = dataframe.index
        self.__dataset_index = 0

    def update_current_dataset(self, scaler):
        current_data_2d = self.__get_current_data_2d()
        self.current_dataset = self.__reshape_features(current_data_2d)
        scaled_values = scaler.fit_transform(current_data_2d)
        self.current_dataset_scaled = self.__reshape_features(scaled_values)
        self.__dataset_index += 1


    def __get_current_data_2d(self):
        return self.dataset[self.__dataset_index  : 
                            self.__batch_size + self.__dataset_index, :]
  

    def __get_dataframe(self, serie, sup_limit_range):
        return self.__builder_io_stacked.dataframe_delays_from_serie(serie,
                                                                     (1, sup_limit_range + 1))
    def __reshape_features(self, array):
        return array.reshape(array.shape[0],
                             self.__steps_delay,
                             self.__n_features)
