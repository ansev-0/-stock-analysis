from src.data_preparation.arima import TransformSerie
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

class AutocorrelationDiagrams:
    def __init__(self, serie):
        self.transform = TransformSerie(serie)
    def plot_acf_diff(self, n, **kwargs):
        plot_acf(self.transform.diff_serie(n, nans=False), **kwargs)

    def plot_pacf_diff(self, n, **kwargs):
        plot_pacf(self.transform.diff_serie(n, nans=False), **kwargs)

    def plot_acf(self, **kwargs):
        plot_acf(self.transform.serie, **kwargs)

    def plot_pacf(self, **kwargs):
        plot_pacf(self.transform.serie, **kwargs)
        