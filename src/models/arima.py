from src.data_preparation.arima import TransformSerie
from statsmodels.tsa.arima_model import ARIMA
import pmdarima.arima as arima
import statsmodels.api as sm


class ArimaModel:
    def __init__(self, train_data, test_data):
        self.__transform = TransformSerie(train_data)
        self.__test_data = test_data


    def auto_arima(self, **kwargs):
        return arima.auto_arima(self.__transform.serie, **kwargs)

    def auto_arima_log(self,**kwargs):
        return arima.auto_arima(self.__transform.log_serie(), **kwargs)

    def sarimax(self, **kwargs):
        return sm.tsa.statespace.SARIMAX(self.__transform.serie, **kwargs)

    def sarimax_log(self, **kwargs):
        return sm.tsa.statespace.SARIMAX(self.__transform.log_serie(), **kwargs)

