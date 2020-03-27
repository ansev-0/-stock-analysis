from src.data_preparation.minmaxscaler import MinMaxScalerFitTransformMany
from src.data_preparation.nn_input_output import BuilderIOStacked
import numpy as np

class CurrentDataSetTarget():

    def __init__(self, serie, batch_size, steps_delay, steps_predict=1, feature_range=(-1, 1)):
        #steps before predict
        self.steps_delay = steps_delay
        # steps to predict
        self.steps_predict = steps_predict
        #range scaler
        self.__feature_range = feature_range
        #batch_size
        self.__batch_size = batch_size
        #builder
        self.builder_io_stacked = BuilderIOStacked()
        #Get dataframe delays
        dataframe = self.__get_dataframe(serie, steps_delay + steps_predict)
        #Get dict with data and target
        self.dataset = self.__get_dataset(dataframe, steps_predict)
        #get the index of temporal time of train
        self.dataset_time_index = dataframe.index
        #init pointer
        self.__dataset_index = 0

        
    def update_current_variables(self):
        # get data to use without scaling
        self.current_data = self.__get_current_data()
        #get data scaled
        self.current_scaled_variables = self.__get_current_scaled_variables()
        #add to next step
        self.__dataset_index += 1
        return None


    def dataset_x(self):
        return self.dataset['x']

    def dataset_y(self):
        return self.dataset['y']

    def current_x(self):
        return self.current_data['x']

    def current_y(self):
        return self.current_data['y']

    def current_scaler_x(self):
        return self.__get_current_scaled('x')[0]

    def current_scaler_y(self):
        return self.__get_current_scaled('y')[0]


    def current_x_scaled(self):
        return self.__get_current_scaled('x')[1]

    def current_y_scaled(self):
        return self.__get_current_scaled('y')[1]


    def __get_current_data(self):
        return {key :  value[self.__dataset_index : self.__batch_size + self.__dataset_index, :]
                             for key, value in self.dataset.items()}

    def __get_current_scaled_variables(self):
        fit_transform_scaler = MinMaxScalerFitTransformMany(self.__feature_range)
        return fit_transform_scaler.dict_array(self.current_data)


    def __get_current_scaled(self, key):
        return self.current_scaled_variables[key]


    def __get_dataframe(self, serie, sup_limit_range):
        return self.builder_io_stacked.dataframe_delays_from_serie(serie,
                                                                        (0, sup_limit_range))
    def __get_dataset(self, *args):
        return self.builder_io_stacked.input_output_from_dataframe_delays(*args)
        
        