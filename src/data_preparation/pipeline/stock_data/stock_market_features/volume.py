from src.data_preparation.pipeline.stock_data.pipeline import PipelineStockData
from src.data_preparation.tools.scale.minmaxscaler import MinMaxScalerFitTransform


class PipelineVolumeStockTimeSerie(PipelineStockData):

    @PipelineStockData.process
    def minmax_scaler_volume(self, volume, feature_range=(-1, 1), *args, **kwargs):
        '''
        This function scales Volume serie
        using the same MinMaxScaler scaler within the range set in feature_range
        '''
        index = volume.index
        scaler, volume = MinMaxScalerFitTransform(feature_range).serie(volume)
        return (scaler, volume, index), None

    @PipelineStockData.process
    def minmax_scaler_volume_with_margins(self, volume, percentage, feature_range=(-1, 1), *args, **kwargs):
        '''
        This function scales Volume serie
        using the same MinMaxScaler scaler within the range set in feature_range
        '''
        index = volume.index
        scaler, volume = MinMaxScalerFitTransform(
            self._get_feature_range_with_margins(feature_range, percentage))\
                .serie(volume, percentage)
        return (scaler, volume, index), {'max_value_scaled' : volume.max(),
                                        'min_value_scaled' : volume.min()}

    @staticmethod
    def _get_feature_range_with_margins(feature_range, percentage):
        return tuple(min(feature_range) + percentage, max(feature_range) + percentage)
