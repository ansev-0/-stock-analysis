import pandas as pd
import numpy as np
from itertools import compress
from src.tools.builders import inlist
from src.tools.check_components import check_equal_lengths



def remove_enumerate_axis(columns):
        if not isinstance(columns,pd.Index):
            columns = pd.Index(columns)
        return columns.str.split('. ').str[-1]

def columns_to_datetime(dataframe,convert=None,columns=None,formats = None):
    df = dataframe.copy()
    
    #Getting columns to change
    if columns is not None: 
        cols_datetime = inlist(columns)
    else:
        cols_datetime = [*df.columns]
    if isinstance(convert,list):
        check_equal_lengths(convert,cols_datetime)
        cols_datetime = list(compress(cols_datetime, convert)) # this filter cols_datetime list

    #Getting formats
    if formats is not None:
        check_equal_lengths(formats,cols_datetime)
        list_formats = formats
    else:
        list_formats=[None]*len(cols_datetime)
        
    #transform to datetime  
    for col,format_col in zip(cols_datetime,list_formats):
        df[col] = pd.to_datetime(df[col], format = format_col)
        
    return df


def monotic_blocks(serie, diff_serie=False):
    serie = serie if diff_serie else serie.diff(-1) 
    signs = np.sign(serie).ffill().mask(lambda sign: sign.eq(0)).ffill()
    blocks = signs.ne(signs.shift()).cumsum()
    return blocks

