import numpy as np
import pandas as pd
from src.data_preparation.tools.expand.stacked_delay import StackedSequencesFromSeries

class MultiFrecuencyStackedSequencesFromSerie(StackedSequencesFromSeries):
    
    def __init__(self, list_frecuencies, list_delays, freq_target='1T', exclude_target=True):

        #Frecuencies
        self._check_valid_frecuencies(list_frecuencies)
        if freq_target not in list_frecuencies:
            self._list_frecuencies.aapend(freq_target)

        self._freq_target = freq_target
        self._int_freq_target = self._get_int_frecuency(freq_target)
        self._list_frecuencies = list_frecuencies
        self._int_frecuencies = self.__map_int_frecuency(list_frecuencies)
        
        #Get min freq
        self.min_frecuency = np.min(self._int_frecuencies)
    
        self._list_delays = list_delays
        self._exclude_target = exclude_target

        #Get max delay
        self._max_delay = self._max_delay_delay(list_frecuencies, list_delays)
        
        #Init stacker
        super().__init__(range(self._max_delay))

    @property
    def frecuencies(self):
        return self._list_frecuencies

    @property
    def delays(self):
        return self._list_delays

    @property
    def freq_target(self):
        return self._freq_target

    @property
    def exclude_target(self):
        return self._exclude_target




#public methods 
    
    def array(self, serie): 
        return self._build_output(*self._array(serie))
        
    def dict_array(self, serie):
        return self._build_dict_output(*self._array(serie), type_output='array')
    
    def frame(self, serie): 
        return self._build_output(*self._frame(serie))
                        
    def dict_frame(self, serie):
        return self._build_dict_output(*self._frame(serie), type_output='dataframe')


#private methods 
                   
    def _array(self, serie):
        array_min_frecuency_to_cut, array_target = self._get_array_min_frecuency(serie)
        list_array = self._list_by_frecuencies_array(array_min_frecuency_to_cut)
        return list_array, array_target

    def _frame(self, serie):
        dataframe_min_frecuency_to_cut, dataframe_target = self._get_dataframe_min_frecuency(serie)
        list_dataframe = self._list_by_frecuencies_dataframe(dataframe_min_frecuency_to_cut)  
        return  list_dataframe, dataframe_target

    def _build_dict_output(self, output_list, output_target, type_output='array'):

        if self._exclude_target:
            return dict(zip(self._list_frecuencies, output_list))

        return dict(dict(zip(self._list_frecuencies, output_list)),
                         **{f'target_{type_output}' : output_target})


    def _build_output(self, output_list, output_target):

        if self._exclude_target:
            return output_list, output_target
        return output_list

    def _get_array_min_frecuency(self, serie):
        array_target=None
        array = self.array_without_nan(serie)
        array_to_cut = array[:, :-self._int_freq_target]

        if not self._exclude_target:
            array_target = array[:, -1:]

        return array_to_cut, array_target
    
    def _get_dataframe_min_frecuency(self, serie):
        dataframe_target = None
        dataframe = self.dataframe_without_nan(serie)
        dataframe_to_cut = dataframe.iloc[:, :-self._int_freq_target]

        if not self._exclude_target:
            dataframe_target = dataframe.iloc[:, [-1]]
            
        return dataframe_to_cut, dataframe_target
            
        
    def _list_frecuencies_array(self, array):
        return [self._cut_array_by_frecuency_and_delay(array, freq, 
                                                       shape_1=array.shape[1])
                for freq in self._int_frecuencies]


    def _cut_array_by_frecuency_and_delay(self, array, freq, shape_1=None):

        if shape_1 is None:
            shape_1 = array.shape[1]
        return array[:, self._boolean_indexing_from_frecuency(shape_1, freq)]\
                     [:, -self._list_delays[self._list_frecuencies.index(freq)]:]
    
    def _list_frecuencies_dataframe(self, dataframe):
        return [self._cut_dataframe_by_frecuency_and_delay(dataframe, freq,
                                                           shape_1=dataframe.shape[1])
                for freq in self._int_frecuencies]

    def _cut_dataframe_by_frecuency_and_delay(self, dataframe, freq, shape_1=None):

        if shape_1 is None:
            shape_1 = array.shape[1]
        return dataframe.loc[:, self._boolean_indexing_from_frecuency(shape_1, freq)]\
                        .iloc[:, -self._list_delays[self._list_frecuencies.index(freq)]:]

    
    def _check_valid_frecuencies(self, list_frecuencies):
        if not np.all(tuple(map(lambda freq: freq.endswith('T'),
                                             list_frecuencies))):
            raise ValueError('You must pass a valid frecuencies')
            
            
    def _map_int_frecuency(self, list_frecuencies):
        return list(map(self._get_int_frecuency, list_frecuencies))
    
    def _max_delay_delay(self, list_frecuencies, list_delays):
        
        max_delay = -1
        for frecuency, delay in zip(self._int_frecuencies, list_delays):
            
            new_product = frecuency * (delay + 1)

            if new_product > max_delay:
                max_delay = new_product
                
        return max_delay


    @staticmethod
    def _boolean_indexing_from_frecuency(shape_1, freq):

        return list(map(lambda index: (index % freq) == 0,
                        np.arange(shape_1))
                        )[::-1]
    
    @staticmethod           
    def _get_int_frecuency(freq):
        return int(freq[:freq.index('T')])
            