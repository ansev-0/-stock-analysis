from src.data_preparation.minmaxscaler import MinMaxScalerFitTransformMany
from src.data_preparation.nn_input_output import BuilderIOStacked
import numpy as np
import pandas as pd

class CurrentDataSetAddFeatures():

    def __init__(self, dataframe, batch_size, steps_delay, feature_range=(-1, 1)):
        self.__batch_size = batch_size
        self.__feature_range = feature_range
        self.steps_delay = steps_delay
        self.n_features = len(dataframe.columns)
        self.builder_io_stacked = BuilderIOStacked()

        dataframe = pd.concat([self.__get_dataframe(serie, steps_delay) for _, serie in dataframe.items()], axis=1)
        self.dataset = dataframe.to_numpy()
        self._dataset_time_index = dataframe.index
        self.__dataset_index  = 0
        
    def update_current_dataset(self, scaler):
        current_data_2d = self.__get_current_data_2d()
        self.current_data = self.__reshape_features(current_data_2d)
        self.current_scaled_data = self.__reshape_features(scaler.transform(current_data_2d))
        self.__dataset_index  += 1
        return None


    def __get_current_data_2d(self):
        return self.dataset[self.__dataset_index  : self.__batch_size + self.__dataset_index , :]
  

    def __get_dataframe(self, serie, sup_limit_range):
        return self.builder_io_stacked.dataframe_delays_from_serie(serie,
                                                                        (1, sup_limit_range + 1))
    def __reshape_features(self, array):
        return array.reshape(array.shape[0], self.steps_delay, self.n_features)