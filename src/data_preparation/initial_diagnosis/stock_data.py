from src.view.figures.time_series import candles
from src.view.figures.time_series.candles import FigureCandlestickManyDataFrame
from src.data_preparation.initial_diagnosis.errors.stock_data \
    import CheckStockDataDiagnosis, CheckManyStockDataDiagnosis
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import seaborn as sns

class StockDataDiagnosis:
    
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self._check_errors = CheckStockDataDiagnosis()
        self._check_errors.check_is_frame(self.dataframe)
        self._check_errors.check_columns(self.dataframe.columns)

    def candlestick_figure(self, **kwargs):
        return go.Figure(data=[candles.Candlestick.\
            from_dataframe(dataframe=self.dataframe[['open', 'high', 'low', 'close']])],
            **kwargs)

    def describe(self, columns=None):
        return self._index_columns(columns)(self.dataframe).describe()

    def missing_values(self, columns=None):
        return sns.heatmap(self._index_columns(columns)(self.dataframe).isnull())

    def missing_values_freq(self, freq):
        return sns.heatmap(self.dataframe.asfreq(freq).isnull())

    def max_time_between_values(self):
        return np.max(self.dataframe.index.to_series().diff())

    def time_between_values(self):
        return self.dataframe.index.to_series().diff().value_counts()

    def hist(self, columns=None, nan=False, **kwargs):
        dataframe=self.dataframe
        if not nan:
            dataframe = self.dataframe.loc[self.dataframe.notnull().all(axis=1)]
        return self._index_columns(columns)(dataframe).plot.hist(*kwargs)

    def plot(self, columns=None, **kwargs):
        return self._index_columns(columns)(self.dataframe).plot(**kwargs)

    def _index_columns(self, columns):
        if not columns:
            return lambda frame: frame
        return lambda frame: frame.loc[:, columns]





class ManyStockDataDiagnosis(StockDataDiagnosis):

    def __init__(self, dataframe):
        super().__init__(dataframe)
        self._check_errors_many = CheckManyStockDataDiagnosis()
        self._check_errors_many.check_columns(self.dataframe.columns)

    def corr(self, columns):
        return self._index_columns(columns)(self.dataframe).corr()

    def candlestick_figure(self, **kwargs):
        return FigureCandlestickManyDataFrame({name : group.droplevel(1, axis=1)
                                               for name, group in 
                                               self.dataframe
                                                   .loc[:, ['open','high','low','close']]
                                                   .groupby(axis=1, level=1)},
                                               **kwargs)

    def _check_errors(self):
        check = CheckManyStockDataDiagnosis()
        self.check_errors.check_columns(self.dataframe.columns)



    


