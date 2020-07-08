from src.data_preparation.tools.expand.stacked_intraday_delay import StackAndMapIntradaySequences
from sklearn.preprocessing import StandardScaler

class ScalerStackedIntradaySequences(StackAndMapIntradaySequences):
    
    @StackAndMapIntradaySequences.stacked_sequences
    def standardscaler(self, array, with_std=False):
        scaler = StandardScaler(with_std=with_std)
        return scaler.fit_transform(array)