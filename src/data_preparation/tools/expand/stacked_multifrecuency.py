import numpy as np
import pandas as pd
from src.data_preparation.tools.expand.stacked_delay import StackedSequencesFromSeries

class MultiFrecuencyStackedSequencesFromSerie(StackedSequencesFromSeries):
    
    def __init__(self, list_frecuencies, list_delays, freq_target='1T', exclude_target=True):
        #check valid frecuencies
        self.__check_valid_frecuencies(list_frecuencies)
        self._list_frecuencies = list_frecuencies
        self._int_frecuencies = self.__map_int_frecuency(list_frecuencies)
        # freq_target
        self._int_freq_target = self._get_int_frecuency(freq_target)
        #get min freq

        self.min_frecuency = np.min(self._int_frecuencies)
        #get max delay
        self._max_length = self.__max_length_delay(list_frecuencies, list_delays)

        self._list_delays = list_delays
       
        self._freq_target = freq_target
        self._exclude_target = exclude_target
        
        #init stacker
        super().__init__(range(self._max_length + np.max(self._list_delays)))
    

    
    
    def list_of_arrays(self, serie):
        
        array_min_frecuency_to_cut, array_target = self.__get_array_min_frecuency(serie)
        list_array = self._cut_by_frecuencies_array(array_min_frecuency_to_cut)
                       
        if self._exclude_target:
            return list_array
        return list_array, array_target
        
    def dict_of_arrays(self, serie):

        array_min_frecuency_to_cut, array_target = self.__get_array_min_frecuency(serie)
        list_array=self._cut_by_frecuencies_array(array_min_frecuency_to_cut)
        
        if self._exclude_target:
            return dict(zip(self._list_frecuencies, list_array))

        return dict(dict(zip(self._list_frecuencies, list_array)), **{'target_array' : array_target})
                        
         
    
    def list_dataframe(self, serie):
                        
        dataframe_min_frecuency_to_cut, dataframe_target = self.__get_dataframe_min_frecuency(serie)
        list_dataframe = self._cut_by_frecuencies_dataframe(dataframe_min_frecuency_to_cut)
            
        if self._exclude_target:
            return list_dataframe
        return list_dataframe, dataframe_target
                        
    def dict_dataframe(self, serie):
        dataframe_min_frecuency_to_cut, dataframe_target = self.__get_dataframe_min_frecuency(serie)

        list_dataframe = self._cut_by_frecuencies_dataframe(dataframe_min_frecuency_to_cut)

                    
        if self._exclude_target:
            return dict(zip(self._list_frecuencies, list_dataframe))

        return dict(dict(zip(self._list_frecuencies, list_dataframe)),
                         **{'target_dataframe' : dataframe_target})

    def __get_array_min_frecuency(self, serie):
        array_target=None
        array = self.array_without_nan(serie)
        array_to_cut = array[:, :-self._int_freq_target]

        if not self._exclude_target:
            array_target = array[:, -1:]

            
        return array_to_cut, array_target
    
    def __get_dataframe_min_frecuency(self, serie):
        dataframe_target = None
        dataframe = self.dataframe_without_nan(serie)

        dataframe_to_cut = dataframe.iloc[:, :-self._int_freq_target]
        if not self._exclude_target:
            
            dataframe_target = dataframe.iloc[:, [-1]]
            
        return dataframe_to_cut, dataframe_target
            
    
    @staticmethod
    def __get_indexes_from_frecuency(shape_1, freq):
        all_indexes = np.arange(shape_1)
        return list(map(lambda index: (index % freq) == 0, all_indexes))[::-1]
        
    def _cut_by_frecuencies_array(self, array):
        shape_1 = array.shape[1]

        return [array[:, self.__get_indexes_from_frecuency(shape_1, freq)]\
                     [:, -self._list_delays[i]:]
                for i, freq in enumerate(self._int_frecuencies)]
    
    def _cut_by_frecuencies_dataframe(self, dataframe):
        shape_1 = dataframe.shape[1]

        return [dataframe.loc[:, self.__get_indexes_from_frecuency(shape_1, freq)]
                         .iloc[: ,-self._list_delays[i]:]
               

                for i, freq in enumerate(self._int_frecuencies)]
    
    def __check_valid_frecuencies(self, list_frecuencies):
        if not np.all(tuple(map(lambda freq: freq.endswith('T'),
                                             list_frecuencies))):
            raise ValueError
            
            
    def __map_int_frecuency(self, list_frecuencies):
        return list(map(self._get_int_frecuency, list_frecuencies))
    
    def __max_length_delay(self, list_frecuencies, list_delays):
        
        max_length = -1
        for frecuency, delay in zip(self._int_frecuencies, list_delays):
            
            new_product = frecuency * delay
            print(new_product)
            if new_product > max_length:
                max_length = new_product
                
        return max_length
    
    @staticmethod           
    def _get_int_frecuency(freq):
        return int(freq[:freq.index('T')])
            