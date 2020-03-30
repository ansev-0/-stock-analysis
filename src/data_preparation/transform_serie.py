from src.tools.reduce_tools import repeated
import pandas as pd
import numpy as np

class TransformSerie:
    def __init__(self, serie):
        self.serie = serie

    def diff_serie(self, n, nans=True):
        series_diff = repeated(pd.Series.diff, n)(self.serie)
        if not nans: 
            series_diff = series_diff.dropna()
        return series_diff

    def log_serie(self):
        return np.log(self.serie)

    def exp_serie(self,serie):
        return np.exp(self.serie)