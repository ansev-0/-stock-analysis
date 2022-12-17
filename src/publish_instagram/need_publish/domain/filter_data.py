import pandas as pd
import numpy as np  
from datetime import timedelta

    
class CalculateDailyCloseChanges:
    
    '''Calculate and filter significative changes in a moment'''

    def __init__(self, serie):
        self._serie = serie
        assert isinstance(self._serie.index, pd.DatetimeIndex)
        self._diff_df = self._calculate_table_incr('diff')
        self._pct_change_df = self._calculate_table_incr('pct_change', freq=None)
               
    @property
    def diff_changes(self):
        return self._diff_df
    
    @property
    def pct_changes(self):
        return self._pct_change_df
    
    def _calculate_table_incr(self, incr_method, **kwargs):
            obj_method = getattr(self._serie, incr_method)
            return pd.concat([obj_method(k, **kwargs).set_axis(pd.MultiIndex.from_tuples(
                                                        list(zip(self._serie.index,
                                                                 np.roll(self._serie.index, k))
                                                            )     
                                                        )
                                                    )
                        for k in range(1, self._serie.shape[0]+1)])\
               .unstack().reindex(columns=self._serie.index).reindex(self._serie.index)\
               .dropna(how='all').dropna(how='all',axis=1)
        
class SelectSignificativeChanges:
    @classmethod
    def from_dataframe_changes(cls, dataframe_changes, min_perc, incr_rate):
        values_incr = np.add(np.arange(dataframe_changes.shape[1]) * incr_rate, min_perc)[::-1]
        values_repeat = np.repeat([values_incr], dataframe_changes.shape[0], axis=0)
        values_repeat = pd.DataFrame(values_repeat, 
                                columns=dataframe_changes.columns, 
                                index=dataframe_changes.index)
        return cls(values_repeat, values_repeat.mul(-1))

    def __init__(self, threshold_pos, threshold_neg):
        self.threshold_pos = threshold_pos
        self.threshold_neg = threshold_neg

    def __call__(self, table):
        return {'big_neg_changes' : table.where(table < self.threshold_neg).stack(),
                'big_pos_changes' : table.where(table > self.threshold_pos).stack()}
    
    
def filter_significative_changes(data, threshold, incr):
    serie = data['close']
    changes = CalculateDailyCloseChanges(serie)
    pos_neg_changes = SelectSignificativeChanges.from_dataframe_changes(changes.pct_changes,
                                                                        threshold,
                                                                        incr)(changes.pct_changes)
    serie_incr = pd.concat(list(pos_neg_changes.values())).rename('incr')
    indices = [i for ind in serie_incr.index for i in ind]
    if not indices:
        return {}
    min_indices = np.min(indices)
    max_indices = np.max(indices)
    min_indices = min_indices if (max_indices-min_indices) > timedelta(days=10) else max_indices - timedelta(days=10) 
    return {'data' : data.loc[min_indices: max_indices, ['open', 'low', 'high', 'close']],
                              'incr': serie_incr}