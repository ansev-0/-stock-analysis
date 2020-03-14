import pmdarima.arima as arima
from src.tools.reduce_tools import repeated
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import pandas as pd
import matplotlib.pyplot as plt

class ArimaModel:
    def __init__(self, serie):
        self.serie=serie

    def auto_arima(self, **kwargs):
        return arima.auto_arima(self.serie, **kwargs)

    def diff(self, n, nans=True):
        series_diff = repeated(pd.Series.diff, n)(self.serie)
        if not nans: 
            series_diff = series_diff.dropna()
        return series_diff

    def plot_acf_diff(self, n, **kwargs):
        plot_acf(self.diff(n, nans=False), **kwargs)

    def plot_pacf_diff(self, n, **kwargs):
        plot_pacf(self.diff(n, nans=False), **kwargs)

    def plot_acf(self, **kwargs):
        plot_acf(self.serie, **kwargs)

    def plot_pacf(self, **kwargs):
        plot_pacf(self.serie, **kwargs)
        