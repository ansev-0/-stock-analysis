from src.data_preparation.pipeline.stock_data.pipeline import PipelineStockData
from src.data_preparation.tools.scale.minmaxscaler import MinMaxScalerFitTransform

class PipelineOriginalStockTimeSerie(PipelineStockData):

    @PipelineStockData.process
    def minmax_scaler_dataframe(self, dataframe, feature_range=(-1, 1), **kwargs):
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
