from src.data_preparation.tools.expand.embedding import EmbedTimeSeries
import numpy as np


class TransformData:
    def __init__(self, delays):
        self.delays = delays

    @property
    def delays(self):
        return self._delays

    @delays.setter
    def delays(self, delays):
        self._delays = delays
        self._mbed = EmbedTimeSeries(delays+1)

    def __call__(self, features):

        sequences = np.diff(self._mbed(features[:-1]), axis=1)
        close_values = features.loc[features.index[-sequences.shape[0]-1:], 'close']
        return sequences, close_values.rename(str).to_dict()