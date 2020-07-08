from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
from src.data_preparation.pipeline.stock_data.pipeline import PipelineStockData
from src.data_preparation.tools.expand.stacked_intraday_delay import StackIntradaySequences




class PipelineOriginalStockIntradayTimeSerie(PipelineStockData):

    @PipelineStockData.process
    def standard_scaler_stacked_sequences(self, dataframe, delays, initial_time, with_std=False):

        '''
        This function scales an intraday series after it is stacked using sklearn preprocessing StandardScaler
        '''
        # Get initial index
        initial_index = dataframe.index

        # Get stacked Array
        array = self._stack_delays(dataframe, delays, initial_time)
        #scale
        scaler = StandardScaler(with_std=with_std)
        array = np.expand_dims(scaler.fit_transform(array.squeeze().T).T, 2)
        # Get final index
        final_index = pd.to_datetime(np.unique(initial_index.date).astype(str))[delays : delays + array.shape[0]]

        return (scaler, array, initial_index, final_index), None

    @staticmethod
    def _stack_delays(dataframe, delays, initial_time):
        return StackIntradaySequences().stack(dataframe=dataframe,
                                               delays=delays, 
                                               initial_time=initial_time)
    