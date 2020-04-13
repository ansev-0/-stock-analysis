from src.tools.reduce_tools import repeated
import pandas as pd
import numpy as np

class TransformSerie:
    def __init__(self, serie):
        self.serie = serie

    def diffn(self, n, nans=True):
        series_diff = repeated(pd.Series.diff, n)(self.serie)
        if not nans: 
            series_diff = series_diff.dropna()
        return series_diff

    def log(self):
        return np.log(self.serie)

    def exp(self,serie):
        return np.exp(self.serie)
    
    
    def inverse_diffn(self, first_n_values):
        
        if  not isinstance(first_n_values, pd.Series):
            sum_serie = pd.Series(index = self.serie.index, data=np.nan)
            
        else:
            sum_serie = first_n_values.reindex_like(self.serie)
            
        sum_serie.loc[self.serie.isna()] = first_n_values
        sum_serie = sum_serie.diff().fillna(sum_serie)
    
        out_serie = out_serie.add(sum_serie, fill_value=0)

        for iloc_index in list(range(len(first_n_values)))[::-1]:
            out_serie.iloc[iloc_index:] = out_serie.iloc[iloc_index:].cumsum()
        return out_serie













