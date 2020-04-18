from src.data_preparation.pipeline.stock_data.pipeline import PipelineStockData
from src.data_preparation.tools.expand.aggregate_dataframe import AggregateWindowRolling
from src.data_preparation.pipeline.stock_data.stock_prices.errors.window \
     import CheckErrors

class PipelineRollingStockTimeSerie(PipelineStockData):
    _check_errors = CheckErrors(AggregateWindowRolling)

    @PipelineStockData.process
    def agg(self, function, serie, agg_values, *args, **kwargs):
        '''
        This function creates a rolling of a series
        with different parameters and aggregates them into a new dataframe.
        '''
        agg_rolling = AggregateWindowRolling(serie)
        self._check_errors.function_implemented(function)
        dataframe = getattr(agg_rolling, function)\
            (agg_values=agg_values, *args, **kwargs).dropna()
            
        return ('not scaler', dataframe, serie.index, dataframe.index), None
