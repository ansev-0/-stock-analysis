from src.exceptions.visualization_exceptions import VisualizationTimeSeriesError
class CheckCandlestickPlotlyTimeSeries:
    
    NAMES_COLUMNS = ['open', 'high', 'low', 'close']

    def check_columns_names(self, dataframe):
        if dataframe.columns.tolist() != self.NAMES_COLUMNS:
            raise VisualizationTimeSeriesError(f'Invalid columns, the columns must be: {self.NAMES_COLUMNS}',
                                                ValueError)
        
