from src.data_preparation.tools.scale.intradaystacked import ScalerStackedIntradaySequences
from src.data_preparation.pipeline.stock_data.pipeline import PipelineStockData
import numpy as np
import pandas as pd

class PipelineFeaturesStockIntradayTimeSerie(PipelineStockData):
    
    @PipelineStockData.process
    def standardscaler_and_stack(self, dataframe, delays, initial_time,  with_std=False):

        '''
        This function stacks and scales intraday data features using StandardScaler.
        '''

        initial_index = dataframe.index
        array = ScalerStackedIntradaySequences().standardscaler(dataframe=dataframe,
                                                                delays=delays, 
                                                                initial_time=initial_time,
                                                                with_std=with_std)


        final_index = pd.to_datetime(np.unique(initial_index.date).astype(str))[delays : delays + array.shape[0]]

        return (None, array, initial_index, final_index), None
