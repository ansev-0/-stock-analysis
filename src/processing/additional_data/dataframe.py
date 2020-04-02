import numpy as np
import pandas as pd
from src.data_preparation.nn_input_output import BuilderIOStacked


class DataSetStackedFeatures():

    def __init__(self, dataframe, samples, steps_delay):
        self.current_dataset = None
        self.current_dataset_scaled = None
        self.__samples = samples
        self.__steps_delay = steps_delay
        self.__n_features = len(dataframe.columns)
        self.__builder_io_stacked = BuilderIOStacked()
        self.dataset = np.stack([self.__get_dataframe(serie, steps_delay).to_numpy()
                                 for _, serie in dataframe.items()],
                                 axis=2)
        #self.dataset_time_index = dataframe.index
        self.__dataset_index = 0

    def update_current_dataset(self, scaler):
        self.current_dataset = self.__get_current_dataset()
        self.current_dataset_scaled = self.__scale_current_dataset(scaler)
        self.__dataset_index += 1


    def __get_current_dataset(self):
        return self.dataset[self.__dataset_index  : 
                            self.__samples + self.__dataset_index, :, :]
  

    def __get_dataframe(self, serie, sup_limit_range):
        return self.__builder_io_stacked.dataframe_delays_from_serie(serie,
                                                                     (1, sup_limit_range + 1))
    def __scale_current_dataset(self, scaler):
        return np.stack([scaler.transform(self.current_dataset[:,:,i]) 
                         for i in range(self.current_dataset.shape[2])],
                         axis=2)
