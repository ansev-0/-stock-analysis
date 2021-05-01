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

        sequences = self.get_sequences(features)
        close_values = features.loc[features.index[-sequences.shape[0]-1:], 'close']
        return sequences, close_values.rename(str).to_dict()

    def get_sequences(self, features):
        return np.diff(self._mbed(features[:-1]), axis=1)


class TransformDataIntraday:
    
    def __init__(self, mbed_conf):
        self._mbed_conf = None
        self.mbed_conf = mbed_conf

    @property
    def mbed_conf(self):
        return self._mbed_conf

    @mbed_conf.setter
    def mbed_conf(self, mbed_conf):
        self._mbed_conf = mbed_conf
        self._mbed = EmbedTimeSeries(**mbed_conf)

    def __call__(self, features):
        return self.get_sequences(features)

    def get_sequences(self, features):
        return self._mbed(features[::-1])[::-1, ::-1]