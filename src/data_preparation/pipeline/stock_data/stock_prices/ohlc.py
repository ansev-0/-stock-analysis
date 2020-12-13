from src.data_preparation.pipeline.stock_data.pipeline import PipelineStockData
from src.data_preparation.pipeline.stock_data.stock_prices.errors.ohlc import CheckErrors
import pandas as pd
import numpy as np

class PipelineBasicTransformOhlc(PipelineStockData):

    _check_errors = CheckErrors()

    @PipelineStockData.process
    def agg(self, dataframe, scaler, func):

        '''
        This function calculates aggregate functions of values ​​open high low and close.
        It also scale the result with input scaler.
        '''
        return self._get_output('agg', dataframe, scaler, func=func)


    @PipelineStockData.process
    def mean(self, dataframe, scaler):
        '''
        This function calculates the mean of the values ​​open high low and close.
        It also scale the result with input scaler.
        '''
        return self._get_output('mean', dataframe, scaler=scaler)


    @PipelineStockData.process
    def var(self, dataframe, scaler):
        '''
        This function calculates the variance of the values ​​open high low and close.
        It also scale the result with input scaler.
        '''
        return self._get_output('var', dataframe, scaler)


    @PipelineStockData.process
    def std(self, dataframe, scaler):
        '''
        This function calculates the std of the values ​​open high low and close.
        It also scale the result with input scaler.
        '''
        return self._get_output('std', dataframe, scaler)

    
    def _get_output(self, function, dataframe, scaler, *args, **kwargs):

        self._check_errors.correct_columns(dataframe)
        self._check_errors.function_implemented(dataframe, function)

        result = getattr(dataframe, function)(*args, **kwargs, axis=1)

        if isinstance(result, pd.DataFrame):
            result = self._scale_dataframe(result, scaler)
        else:
            result = self._scale_serie(result, scaler).rename(function)

        index = dataframe.index
        return ('input scaler', result, index), {'max_values_scaled' : result.max(),
                                                 'min_values_scaled' : result.min()}

    @staticmethod
    def _scale_serie(serie, scaler):
        return pd.Series(data=scaler.transform(serie.values[:, None]).squeeze(), index=serie.index)


    @staticmethod
    def _scale_dataframe(dataframe, scaler):
        return pd.DataFrame(data=np.hstack([scaler.transform(col.values[:, None])
                                            for _,col in dataframe.items()]),
                            index=dataframe.index,
                            columns=dataframe.columns)





        