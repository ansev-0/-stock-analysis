from src.data_preparation.pipeline.stock_data.pipeline import PipelineStockData
from src.data_preparation.tools.expand.aggregate_dataframe import AggregateWindowEwm
from src.data_preparation.pipeline.stock_data.stock_prices.errors.window \
     import CheckErrors



class PipelineEwmStockTimeSerie(PipelineStockData):
    _check_errors = CheckErrors(AggregateWindowEwm)

    @PipelineStockData.process
    def agg(self, function, serie, agg_values, *args, **kwargs):
        '''
        This function creates an exponential smoothing of a series
        with different parameters and aggregates them into a new dataframe.
        '''
        agg_ewm = AggregateWindowEwm(serie)
        self._check_errors.function_implemented(function)
        dataframe = getattr(agg_ewm, function)(agg_values=agg_values, *args, **kwargs)
        return ('not scaler', dataframe, serie.index), None

