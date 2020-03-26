import pandas as pd
import numpy as np

class BuilderIOStacked:

    def __init__(self):
        self.keys = ('x', 'y')

    def dataframe_delays_from_serie(self, serie, first_delay, last_delay):
        return pd.concat([serie.shift(i).rename(f'Serie_delay_{i}') 
                          for i in range(first_delay, last_delay + 1)], axis=1).dropna()     

    def input_output_from_dataframe_delays(self, dataframe, col_start_input):
        return {by : group.to_numpy() 
                for by, group in dataframe.groupby(by=np.where(
                    np.arange(len(dataframe.columns)) >= col_start_input,
                    *self.keys), axis=1)}
                    
