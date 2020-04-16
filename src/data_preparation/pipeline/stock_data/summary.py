from src.data_preparation.pipeline.summary import Summary


class SummaryStockData(Summary):

    
    @Summary.register
    def enter_params(self, initial_index, final_index,
                     scaler, transform_functions,
                     **kwargs):
        return (initial_index, final_index, scaler, transform_functions), kwargs



