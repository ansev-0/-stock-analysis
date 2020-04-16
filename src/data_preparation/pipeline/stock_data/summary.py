from src.data_preparation.pipeline.summary import Summary

class SummaryStockData(Summary):

    
    @Summary.register
    def enter_params(self, initial_index, final_index, scaler, transform_functions, **kwargs):
        return (initial_index, final_index, scaler, transform_functions), kwargs

    def build(self):
        pass

summary = SummaryStockData()
summary.enter_params(1,2,3,4,5, data=4)
print(summary.registry)
    