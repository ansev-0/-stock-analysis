import numpy as np
import pandas as pd
from src.data_preparation.tools.expand.stacked_delay import StackedSequencesFromSeries
from functools import wraps

class MultiFrecuencyStackedSequencesFromSerie(StackedSequencesFromSeries):
    
    def __init__(self, list_frecuencies, list_delays, freq_target='1T', exclude_target=None):

        #Frecuencies
        self._check_valid_frecuencies(list_frecuencies)
        self._list_frecuencies = list_frecuencies

        if freq_target not in list_frecuencies:
            self._list_frecuencies.append(freq_target)

        self._freq_target = freq_target
        self._int_freq_target = self._get_int_frecuency(freq_target)
        
        self._int_frecuencies = self._map_int_frecuency(list_frecuencies)
        
        #Get min freq
        self.min_frecuency = np.min(self._int_frecuencies)
    
        self._list_delays = list_delays
        self._exclude_target = exclude_target

        #Get max delay
        self._max_delay = self._get_max_delay(list_frecuencies, list_delays)
        
        #Init stacker
        super().__init__(range(self._max_delay + self._int_freq_target + 1))

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
    def int_freq_target(self):
        return self._int_freq_target

    @property
    def exclude_target(self):
        return self._exclude_target

    @property
    def max_delay(self):
        return self._max_delay


    @exclude_target.setter
    def exclude_target(self, exclude_target):
        if exclude_target is not None:
            self._exclude_target = exclude_target



    @classmethod
    def wrap_stack_and_resample(cls, type_output):

        def wrap_function(function):

        #function for dataframe
            @wraps(function)
            def stack_resample_and_map_dataframe(self, dataframe, freq, dataframe_target=None, **kwargs):

                dataframe_resample_cut = self._cut_dataframe_by_frecuency_and_delay(dataframe,
                                                                                    freq, dataframe.shape[1])

                if dataframe_target is not None:
                    return function(self, dataframe_resample_cut, dataframe_target,  **kwargs)

                return function(self, dataframe_resample_cut,  **kwargs)


            #function for array
            @wraps(function)
            def stack_resample_and_map_array(self, array, freq, array_target=None, **kwargs):

                array_resample_cut = self._cut_array_by_frecuency_and_delay(array,
                                                                            freq, array.shape[1])

                if array_target is not None:
                    result = function(self, array_resample_cut, array_target,  **kwargs)
                    return result

                return function(self, array_resample_cut,  **kwargs)

            #Return function
            if type_output == 'array':
                return stack_resample_and_map_array

            elif type_output == 'dataframe':
                return stack_resample_and_map_dataframe
            else:
                raise ValueError('Invalid type_output, you must pass array or dataframe')

        return wrap_function

#instance public methods
    
    def arrays(self, serie, exclude_target=None): 
        self.exclude_target = exclude_target
        return self._build_output(*self._array(serie))
        
    def dict_arrays(self, serie, exclude_target=None):
        self.exclude_target = exclude_target
        return self._build_dict_output(*self._array(serie), type_output='array')
    
    def frames(self, serie, exclude_target=None): 
        self.exclude_target = exclude_target
        return self._build_output(*self._frame(serie))
                        
    def dict_frames(self, serie, exclude_target=None):
        self.exclude_target = exclude_target
        return self._build_dict_output(*self._frame(serie), type_output='dataframe')


#instance private methods 
                   
    def _array(self, serie):
        array_min_frecuency_to_cut, array_target = self._get_array_min_frecuency(serie)
        list_array = self._list_frecuencies_array(array_min_frecuency_to_cut)
        return list_array, array_target

    def _frame(self, serie):
        dataframe_min_frecuency_to_cut, dataframe_target = self._get_dataframe_min_frecuency(serie)
        list_dataframe = self._list_frecuencies_dataframe(dataframe_min_frecuency_to_cut)  
        return  list_dataframe, dataframe_target

    def _build_dict_output(self, output_list, output_target, type_output='array'):

        if self._exclude_target:
            return dict(zip(self._list_frecuencies, output_list))

        return dict(dict(zip(self._list_frecuencies, output_list)),
                         **{f'target_{type_output}' : output_target})


    def _build_output(self, output_list, output_target):

        if not self._exclude_target:
            return output_list, output_target
        return output_list

    def _get_array_min_frecuency(self, serie):
        array_target=None
        array = self.array_without_nan(serie)
        if not self._exclude_target:
            array_target = array[:, -1:]

        return array, array_target
    
    def _get_dataframe_min_frecuency(self, serie):
        dataframe_target = None
        dataframe = self.dataframe_without_nan(serie)

        if not self._exclude_target:
            dataframe_target = dataframe.iloc[:, [-1]].copy()

        return dataframe, dataframe_target
            
        
    def _list_frecuencies_array(self, array):
        return [self._cut_array_by_frecuency_and_delay(array, freq, 
                                                       shape_1=array.shape[1])
                for freq in self._int_frecuencies]



    def _cut_array_by_frecuency_and_delay(self, array, freq, shape_1=None):

        if shape_1 is None:
            shape_1 = array.shape[1]
        size = self._list_delays[self._int_frecuencies.index(freq)] * freq

        return array[:, -size - self._int_freq_target : -self._int_freq_target : freq]

    def _list_frecuencies_dataframe(self, dataframe):
        return [self._cut_dataframe_by_frecuency_and_delay(dataframe, freq,
                                                           shape_1=dataframe.shape[1])
                for freq in self._int_frecuencies]

    def _cut_dataframe_by_frecuency_and_delay(self, dataframe, freq, shape_1=None):
        
        if shape_1 is None:
            shape_1 = dataframe.shape[1]
        size = self._list_delays[self._int_frecuencies.index(freq)] * freq

        return dataframe.iloc[:, -size -self._int_freq_target : -self._int_freq_target:freq]


     
    def _check_valid_frecuencies(self, list_frecuencies):
        if not np.all(tuple(map(lambda freq: freq.endswith('T') | freq.endswith('M'),
                                             list_frecuencies))):
            raise ValueError('You must pass a valid frecuencies')
            
            
    def _map_int_frecuency(self, list_frecuencies):
        return list(map(self._get_int_frecuency, list_frecuencies))
    
    def _get_max_delay(self, list_frecuencies, list_delays):
        
        max_delay = -1

        for frecuency, delay in zip(self._int_frecuencies, list_delays):
            new_product = frecuency * delay 
            if new_product > max_delay:
                max_delay = new_product
                
        return max_delay
    
    @staticmethod           
    def _get_int_frecuency(freq):
        return int(freq[:freq.index('T')])
            

class MultiFrecuencyScaleAndStackSequences(MultiFrecuencyStackedSequencesFromSerie):

    @classmethod
    def wrap_from_serie(cls, type_output, save_in='list'):


        def wrap_function_serie(function, *args, **kwargs):

            function_to_cut_and_map = MultiFrecuencyStackedSequencesFromSerie.wrap_stack_and_resample(type_output=type_output)(function)

            @wraps(function)
            def from_serie(self, serie, exclude_target=None, scale_target=True, **kwargs):

                #save exclude target for this serie
                self.exclude_target = exclude_target

                #get data stacked
                data_to_cut, data_target = self._get_stacked_data(serie, type_output)


                list_data_cut_and_map = []

                cond = scale_target and (not self.exclude_target)

                #resample and cut
                for freq in self._int_frecuencies:

                    #pass target to scale if neccesary
                    if cond and (freq == self._int_freq_target):
                        data_for_freq, data_target, scaler = function_to_cut_and_map(self, 
                                                                                     data_to_cut,
                                                                                     freq,
                                                                                     data_target,
                                                                                     **kwargs)
                    else:
                        data_for_freq = function_to_cut_and_map(self, data_to_cut, freq, **kwargs)

                    list_data_cut_and_map.append(data_for_freq)

                if save_in == 'list':
                    output = self._build_output(list_data_cut_and_map, data_target)

                elif save_in=='dict':
                    output = self._build_dict_output(list_data_cut_and_map, data_target)

                else:
                    raise ValueError('Invalid type_output, you must pass list or dict')


                if cond:
                        return output, scaler
                return output

            return from_serie

        return wrap_function_serie


    @classmethod
    def wrap_array3d_from_dataframe(cls, save_in='list'):

 
        def wrap_function_frame(function, *args, **kwargs):

            function_to_cut_and_map = MultiFrecuencyStackedSequencesFromSerie.wrap_stack_and_resample(type_output='array')(function)

            @wraps(function)
            def from_frame(self, dataframe, exclude_target=None, scale_target=True, target_label=None, **kwargs):
                #resample and cut
                list_arrays_3d = []
                for freq in self._int_frecuencies:

                    list_arrays2d_cut_and_map = []
                    for name_col, serie in dataframe.items():

                        #save exclude target for this serie
                        if name_col == target_label:
                            self.exclude_target = exclude_target
                        else:
                            self.exclude_target = True

                        #get data stacked

                        array_to_cut, array_target = self._get_array_min_frecuency(serie)
                        cond = scale_target and (not self.exclude_target)

                        #pass target to scale if neccesary
                        if cond and (freq == self._int_freq_target):
                            array_for_freq_col, array_target, scaler = function_to_cut_and_map(self, 
                                                                                               array_to_cut,
                                                                                               freq,
                                                                                               array_target,
                                                                                               **kwargs)
                        else:  
                            array_for_freq_col = function_to_cut_and_map(self, array_to_cut, freq, **kwargs)

                        list_arrays2d_cut_and_map.append(array_for_freq_col)
                    
                    list_arrays_3d.append(np.stack(list_arrays2d_cut_and_map, axis=2))

                if save_in == 'list':
                    output = self._build_output(list_arrays_3d, array_target)

                elif save_in=='dict':
                    output = self._build_dict_output(list_arrays_3d, array_target)

                else:
                    raise ValueError('Invalid type_output, you must pass list or dict')


                if cond:
                        return output, scaler

                return output


            return from_frame

        return wrap_function_frame


    def _get_stacked_data(self, serie, type_output):

        if type_output == 'dataframe':
            data_to_cut, data_target = self._get_dataframe_min_frecuency(serie)


        elif type_output == 'array':
            data_to_cut, data_target = self._get_array_min_frecuency(serie)
        else:
            raise ValueError('Invalid type_output, you must pass dataframe or array')

        return data_to_cut, data_target




