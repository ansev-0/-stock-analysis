
import pandas as pd
import numpy as np
from src.read_database.stock_data import StockDataFromDataBase as reader

from pymongo import MongoClient
from src.data_preparation.tools.resample.ohlcv import ResampleOhlcDataFrame
from src.data_preparation.tools.fill_missing_values.bygroups import FillByPeriods
from src.data_preparation.tools.expand.stacked_delay import  StackedSequencesFromSeries
from src.data_preparation.tools.expand.aggregate_dataframe import AggregateWindowEwm, AggregateWindowRolling
from src.data_preparation.tools.scale.intradaystacked import MultiFrecuencyStandardScaleAndStackSequences
from src.data_preparation.tools.split.io_dataset_split import SplitIO
from sklearn.preprocessing import StandardScaler

def check_not_incomplete_days(df):

    assert (df.isnull().any(axis=1)
              .groupby(pd.Grouper(freq='1D'))
              .sum().value_counts().index
              .isin([0, 390]).all())
    
def check_max_diff_days(df, max_days):
    assert df.index.to_series().diff().max() <= pd.Timedelta(f'{max_days}D')
    
    
def get_dates_with_open_market(df):
    return (df.asfreq('1T')
              .between_time('09:31', '16:00')
              .loc[lambda df: df.index.weekday.isin(range(5))])
    
    
def clean_dataframe_1min(df, max_days_with_market_close=2):
    
    ohlc_columns = ['close', 'open', 'high', 'low']
    
    #get rows of open market
    df = get_dates_with_open_market(df)
    
    #get blocks of nulls
    blocks = df.notnull().all(axis=1).cumsum()
    # get groups by blocks and day
    groups = df.groupby([pd.Grouper(freq='1D'), blocks])
    
    #get values to fill missing values by groups
    last_value_before_nan = groups['close'].transform('first')
    previous_value_before_nan = (groups['open'].transform('first')
                                               .groupby(pd.Grouper(freq='1D'))
                                               .bfill())
    #fill missing values
    df_1min = df.assign(**{name : col.fillna(last_value_before_nan.\
                                             combine_first(previous_value_before_nan)) 
                           for name, col in df[ohlc_columns].items()})
    
    df_1min['volume'] = df['volume'].fillna(0)

    #check complete days   
    check_not_incomplete_days(df_1min)
    #check max_diff_days
    check_max_diff_days(df_1min, max_days_with_market_close)
    
    df_1min = df_1min.dropna()
    
    
    return df_1min

def prepare_dataframe(dataframe, freq, add_cols=None, dataframe_freq='T', delay_tolerance=None):
    
    if freq == dataframe_freq:
        return dataframe
    else:
        df = ResampleOhlcDataFrame(freq).resample(dataframe, add_cols=add_cols)\
            .between_time('09:30', '15:59')
    
    if delay_tolerance == 0:
        df=FillByPeriods('D').ffill(df)
    else:
        df=FillByPeriods('D').fbfill(df, b_limit=delay_tolerance)
    df = df.dropna()
    
    assert len(df.index.to_series().dt.date.value_counts().unique())
    
    return df

def get_data_from_base(company, init_date, last_date, reader=reader):
    reader = reader.intraday_dataframe('1min')
    return reader.get(stock=company, start = init_date, end=last_date)

def split_train_and_test_serie(serie, test_rows, delays, freq_target):
    return serie[:-test_rows], serie[-test_rows - delays - freq_target:]


def split_list_arrays_train_and_test(list_array, test_rows, l_train, l_test):
    for arr in list_array:
        train, test = split_train_and_test(arr, test_rows)
        l_train.append(train), l_test.append(test)
    return l_train, l_test



def split_train_and_test(data, test_samples):
    return data[:-test_samples], data[-test_samples:] 


def get_real_test_values(dataframe, test_rows, shift_n_values=1):

    return dataframe.loc[:, ['close']][-shift_n_values-test_rows:]






def generate_train_and_test_data(company,
                                 init_date, 
                                 last_date,
                                 delays, 
                                 frecuencies_features,
                                 frecuency_target,
                                 test_rows):
    

    ewm_values = list(range(1, 15, 2)) + list(range(20, 70, 10))
    range_rolling = range(2, 10)
    #get data from database
    df = get_data_from_base(company, init_date, last_date)
    df_1min = clean_dataframe_1min(df, max_days_with_market_close=4)


    df_agg = AggregateWindowEwm(df_1min['close']).mean(ewm_values)
    df_rolling = AggregateWindowRolling(df_1min['close']).mean(range_rolling).dropna()
    df_1min = pd.concat([df_1min, df_agg, df_rolling], axis=1, join='inner')


    #sequences target
    target_df = prepare_dataframe(df_1min, '1T', add_cols=['last']).droplevel(axis=1, level=1)

    #procces 
    procces = MultiFrecuencyStandardScaleAndStackSequences(list_frecuencies=[frecuency_target] + frecuencies_features,
                                                             list_delays=delays, 
                                                             freq_target=frecuency_target, 
                                                             exclude_target=False)

    int_freq_target = procces.int_freq_target
    max_delay = procces.max_delay

    #get real values
    df_real = get_real_test_values(target_df, test_rows, int_freq_target)
    #take log1p
    target_df = np.log1p(target_df)



    #target serie

    close_train, close_test = split_train_and_test_serie(target_df['close'], test_rows, max_delay, int_freq_target)

    data_close_train, scaler_train = procces.arrays_scaled_from_serie(serie=close_train, scale_target=True)
    x_close_train , Y_train = data_close_train

    data_close_test, scaler_test = procces.arrays_scaled_from_serie(serie=close_test, scale_target=True)
    x_close_test , Y_test = data_close_test

    procces.exclude_target = True


    df_ewm = target_df.filter(regex = 'ewm')
    x_ewm = procces.arrays_scaled_from_dataframe(df_ewm, scale_target=False)

    df_rolling = target_df.filter(regex = 'rolling')
    x_rolling = procces.arrays_scaled_from_dataframe(df_rolling, scale_target=False)


    X_train = [np.expand_dims(arr, 2) for arr in x_close_train]
    X_test = [np.expand_dims(arr, 2) for arr in x_close_test]
    
    X_train, X_test = split_list_arrays_train_and_test(x_ewm, test_rows, X_train, X_test)
    X_train, X_test = split_list_arrays_train_and_test(x_rolling, test_rows, X_train, X_test)

    return X_train, Y_train, X_test, Y_test, scaler_test, df_real

