import numpy as np
from functools import wraps


class StackAndMapIntradaySequences:
    
    @classmethod
    def stacked_sequences(cls, function):
        
        @wraps(function)
        def map_and_stack(self, dataframe, delays, initial_time=None, **kwargs):
            
            index = dataframe.index
            #cut if it is specified else 0
            cut_end_day = 0
            if initial_time:
                dataframe, cut_end_day = self._cut_by_initial_time(dataframe, initial_time)
            
            #get constants
            n_rows_in_period, n_dates, len_seq = self._get_n_constants(index, delays)
            total_rows_to_index = (n_dates - delays - cut_end_day) * n_rows_in_period
            
            #apply a function in each sequence array of shape 2 and stack it
            if delays > 1:
                return np.stack([function(self, dataframe[n:  n + len_seq], **kwargs)
                                for n in range(0, total_rows_to_index , n_rows_in_period)])

            else:

                return np.stack([function(self, group, **kwargs) 
                                 for _, group in dataframe.groupby(np.arange(len(dataframe)) // len_seq)])

            
        return map_and_stack

    
    @staticmethod
    def _get_n_constants(index, days_of_delay):
        
        #get dates index
        dates = index.to_series().dt.date
        
        # get unique n rows by days
        unique_n_values_by_days = dates.value_counts().unique()
        
        #check all days has the same number of rows
        assert len(unique_n_values_by_days) == 1 
        
        # Get n of days
        n_dates = len(dates.unique())
        
        #Get rows by days
        n_rows_in_day = unique_n_values_by_days[0]
        
        # Len Sequences
        len_seq = days_of_delay * n_rows_in_day
        
        return n_rows_in_day, n_dates, len_seq
    
        
    @staticmethod   
    def _cut_by_initial_time(dataframe, time):
        mask = (dataframe.index.time.astype(str) == time).cumsum() > 0
        dataframe = dataframe.loc[mask]
        return dataframe, int(~mask.all())


class StackIntradaySequences(StackAndMapIntradaySequences):
    
    @StackAndMapIntradaySequences.stacked_sequences
    def stack(self, slice_dataframe):
        return slice_dataframe


