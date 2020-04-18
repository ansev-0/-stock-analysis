from src.data_preparation.pipeline.stock_data.pipeline import PipelineStockData
from src.data_preparation.pipeline.stock_data.stock_prices.errors.ohlc import CheckErrors

class PipelineBasicTransformOhlc(PipelineStockData):

    _check_errors = CheckErrors()

    @PipelineStockData.process
    def agg(self, dataframe, func):
        print(dataframe)
        '''
        This function calculates aggregate functions of values ​​open high low and close.
        '''
        return self._get_output('agg', dataframe, func=func)


    @PipelineStockData.process
    def mean(self, dataframe):
        '''
        This function calculates the mean of the values ​​open high low and close.
        '''
        return self._get_output('mean', dataframe)


    @PipelineStockData.process
    def var(self, dataframe):
        '''
        This function calculates the variance of the values ​​open high low and close.
        '''
        return self._get_output('var', dataframe)


    @PipelineStockData.process
    def std(self, dataframe):
        '''
        This function calculates the std of the values ​​open high low and close.
        '''
        return self._get_output('std', dataframe)

    
    def _get_output(self, function, dataframe, *args, **kwargs):
        self._check_errors.correct_columns(dataframe)
        self._check_errors.function_implemented(dataframe, function)

        result = getattr(dataframe, function)(*args, **kwargs, axis=1)
        index = dataframe.index
        return ('not scaler', result, index), None

        