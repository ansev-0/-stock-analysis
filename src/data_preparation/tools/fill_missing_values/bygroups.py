import pandas as pd

class FillByPeriods:

    def __init__(self, freq):
        self.freq=freq

    @property
    def freq(self):
        return self._freq
    
    @freq.setter
    def freq(self, freq):
        self._freq=freq
        self._by =pd.Grouper(freq=self._freq)

    def ffill(self, dataframe, *args, **kwargs):
        return self._groups(dataframe).ffill(*args, **kwargs)

    def bfill(self, dataframe, *args, **kwargs):
        return self._groups(dataframe).bfill(*args, **kwargs)
        return dataframe.groupby(pd.Grouper(freq=self.freq))
    
    def fbfill(self, dataframe, f_limit=None, b_limit=None):
        return self._groups(dataframe).apply(lambda group: group.ffill(limit=f_limit).bfill(limit=b_limit))


    def _groups(self, dataframe):
        return dataframe.groupby(by=self._by)