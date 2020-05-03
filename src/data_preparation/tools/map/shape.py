import pandas as pd
import numpy as np

def map_len_columns(list__pandas_objects):
    return map(lambda item: len(item.columns) if isinstance(item, pd.DataFrame) else 1,
            list__pandas_objects)

def cumsum_len_columns(list__pandas_objects):
    return np.cumsum(tuple(map_len_columns(list__pandas_objects)))