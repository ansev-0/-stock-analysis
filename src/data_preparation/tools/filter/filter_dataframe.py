

class DataFrameInspectNull:
    def __init__(self, dataframe):
        self.dataframe = dataframe
    
    def has_n_null(self, n, axis=0):
        return self.count_null(axis=axis).ge(n)
    
    def count_null(self, axis=0):
        return self.dataframe.isnull().sum(axis=axis)
    

    
class FilterDataFrameNull(DataFrameInspectNull):
    
    def remove_continuous_null(self, ge, limit_null=None, axis=0):
        if not limit_null:
            notnull_mask = self.dataframe.notnull().all(axis=axis)
        else:
            notnull_mask = ~self.has_n_null(limit_null+1 ,axis=axis)
        blocks = notnull_mask.cumsum()
        blocks_filter = (blocks.map(blocks.value_counts())
                               .sub(blocks.clip(upper=1))
                               .lt(ge))
        filter_mask = blocks_filter | notnull_mask
        if axis:
            return self.dataframe.loc[filter_mask, :]
        return self.dataframe.loc[:, filter_mask]



def filter_open_market_hours(dataframe):
    return dataframe.between_time('09:30', '16:00')
        
