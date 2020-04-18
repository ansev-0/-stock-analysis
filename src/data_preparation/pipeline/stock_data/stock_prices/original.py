from src.data_preparation.pipeline.stock_data.pipeline import PipelineStockData
from src.data_preparation.tools.scale.minmaxscaler import MinMaxScalerFitTransform


class PipelineOriginalStockTimeSerie(PipelineStockData):

    @PipelineStockData.process
    def minmax_scaler_dataframe(self, dataframe, feature_range=(-1, 1)):
        '''
        This function scales all the values ​​in the DataFrame
        using the same MinMaxScaler scaler within the range set in feature_range
        '''
        index = dataframe.index
        scaler, dataframe = MinMaxScalerFitTransform(feature_range).dataframe(dataframe)
        return (scaler, dataframe, index), None

    @PipelineStockData.process
    def minmax_scaler_serie(self, serie, feature_range=(-1, 1)):
        '''
        This function scales all the values ​​in the Serie
        using the same MinMaxScaler scaler within the range set in feature_range
        '''
        index = serie.index
        scaler, serie = MinMaxScalerFitTransform(feature_range).serie(serie)
        return (scaler, serie, index), None


    @PipelineStockData.process
    def minmax_scaler_dataframe_with_margins(self, dataframe, 
                                             percentage, feature_range=(-1, 1)):
        '''
        This function scales all the values ​​in the DataFrame
        using the same MinMaxScaler scaler within the range set in feature_range
        '''
        index = dataframe.index
        scaler, dataframe = MinMaxScalerFitTransform(
            self._get_feature_range_with_margins(feature_range, percentage))\
                .dataframe(dataframe, percentage)
        return (scaler, dataframe, index), {'max_values_scaled' : dataframe.max(),
                                            'min_values_scaled' : dataframe.min()}

    @PipelineStockData.process
    def minmax_scaler_serie_with_margins(self, serie,
                                         percentage, feature_range=(-1, 1)):
        '''
        This function scales all the values ​​in the Serie
        using the same MinMaxScaler scaler within the range set in feature_range
        '''
        index = serie.index
        scaler, serie = MinMaxScalerFitTransform(
            self._get_feature_range_with_margins(feature_range, percentage))\
                .serie(serie, percentage)
        return (scaler, serie, index), {'max_value_scaled' : serie.max(),
                                        'min_value_scaled' : serie.min()}

    @staticmethod
    def _get_feature_range_with_margins(feature_range, percentage):
        return tuple(min(feature_range) + percentage,
                     max(feature_range) + percentage)
                     