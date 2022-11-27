import pandas as pd
import numpy as np

class CalculateDailyCloseChanges:
    
    '''Calculate significative changes in between days'''

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
            return pd.concat([obj_method(k, **kwargs).set_axis(
                pd.MultiIndex.from_tuples(
                                            list(zip(self._serie.index,
                                                     np.roll(self._serie.index, k))
                                            )     
                                        )
                )
                                for k in range(1, self._serie.shape[0]+1)])\
                     .unstack()\
                     .reindex(columns=self._serie.index).reindex(index=self._serie.index)\
                     .dropna(how='all').dropna(how='all',axis=1)
        
    
class SignificativeChanges:
    ''' Detect significative changes based on threshold '''
    def __init__(self, threshold_diff, threshold_pct_changes):
        self._threshold_diff=threshold_diff
        self._threshold_pct_changes=threshold_pct_changes
        
    def __call__(self, table_diff_changes, table_pct_changes):
        return (table_diff_changes.abs() > self._threshold_diff,
               table_pct_changes > self._threshold_pct_changes)    