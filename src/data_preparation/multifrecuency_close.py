
import pandas as pd
import numpy as np
from src.read_database.stock_data import StockDataFromDataBase as reader

from pymongo import MongoClient
from src.data_preparation.tools.resample.ohlcv import ResampleOhlcDataFrame
from src.data_preparation.tools.fill_missing_values.bygroups import FillByPeriods
from src.data_preparation.tools.expand.stacked_delay import  StackedSequencesFromSeries
from src.data_preparation.tools.expand.aggregate_dataframe import AggregateWindowEwm, AggregateWindowRolling
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

def get_stacked_sequences(serie, delay, not_include_target=True):
    return (StackedSequencesFromSeries(range_delays=range(int(not_include_target),
                                                          delay + 1)).dataframe_without_nan(serie))

def scale_x_data(dataframe):
    scaler = StandardScaler(with_std=False)
    return np.expand_dims(scaler.fit_transform(dataframe.to_numpy().T).T, 2), scaler

def scale_y_data(dataframe, scaler):
    return scaler.transform(dataframe.to_numpy().T).T

def split_train_and_test(data, test_samples):
    return data[:-test_samples], data[-test_samples:] 


def get_real_test_values(dataframe, test_rows):
    return dataframe.loc[:, ['close']][-test_rows:]

def append_train_and_test_arrays(dict_sequences, test_rows, x_train, x_test):

    for sequence in dict_sequences.values():
        train_sequences, test_sequences = split_train_and_test(sequence, test_rows)
        x_train.append(train_sequences)
        x_test.append(test_sequences)

    return x_train , x_test

def stack_filter_scale_and_concatenate_features(dataframe, delay, index):
    return np.concatenate([scale_x_data(get_stacked_sequences(serie, delay)\
                           .loc[index])[0] 
                           for _, serie in dataframe.items()], axis=2) 


def generate_train_and_test_data(company,
                                 init_date, 
                                 last_date,
                                 delay, 
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
    target_df = np.log1p(prepare_dataframe(df_1min, frecuency_target, add_cols=['last']))
    sequences_target = get_stacked_sequences(target_df['close'], 
                                             delay,
                                             not_include_target = False)
    index_target = sequences_target.index

  
    sequences_target_features_rolling = stack_filter_scale_and_concatenate_features(target_df.droplevel(level=1, axis=1)
                                                                                             .filter(regex='rolling'),
                                                                                    delay, 
                                                                                    index_target)


    sequences_target_features_ewm = stack_filter_scale_and_concatenate_features(target_df.droplevel(level=1, axis=1)
                                                                                         .filter(regex='ewm'),
                                                                                delay,
                                                                                index_target)


    #others frecuency sequences
    dict_others_frecuencies_close_log1p = {}
    dict_df_others_frecuencies_features_log1p_rolling, dict_df_others_frecuencies_features_log1p_ewm = {}, {}

    for freq in frecuencies_features:
        dataframe = np.log1p(prepare_dataframe(df_1min, freq, add_cols=['last'])).droplevel(1, axis=1)
        dict_others_frecuencies_close_log1p[freq] = dataframe['close']
        dict_df_others_frecuencies_features_log1p_rolling[freq] = dataframe.filter(regex='rolling')
        dict_df_others_frecuencies_features_log1p_ewm[freq] = dataframe.filter(regex='ewm')


    dict_sequences_others_frecuencies_close = {freq : scale_x_data(get_stacked_sequences(serie, delay)
                                                                   .loc[sequences_target.index])[0] 
                                               for freq, serie in dict_others_frecuencies_close_log1p.items()}

    dict_sequences_others_frecuencies_features_rolling = {freq : stack_filter_scale_and_concatenate_features(dataframe, delay, index_target) 
                                                          for freq, dataframe in \
                                                          dict_df_others_frecuencies_features_log1p_rolling.items()}

    dict_sequences_others_frecuencies_features_ewm = {freq :  stack_filter_scale_and_concatenate_features(dataframe, delay, index_target)
                                                          for freq, dataframe in \
                                                          dict_df_others_frecuencies_features_log1p_ewm.items()}

    # Get target arrays
    train_target_sequences, test_target_sequences = split_train_and_test(sequences_target, test_rows)

    spliter_io = SplitIO(1)
      # train
    X_train_target, Y_train = spliter_io.tuple_from_frame(train_target_sequences)
    X_train_target, scaler_x_train_target = scale_x_data(X_train_target)
    Y_train = scale_y_data(Y_train, scaler_x_train_target)

      # Test
    X_test_target, Y_test = spliter_io.tuple_from_frame(test_target_sequences)
    X_test_target, scaler_x_test_target = scale_x_data(X_test_target)
    Y_test = scale_y_data(Y_test, scaler_x_test_target)


    X_train = [X_train_target]
    X_test = [X_test_target]


    train_sequences, test_sequences = split_train_and_test(sequences_target_features_rolling, test_rows)
    X_train.append(train_sequences)
    X_test.append(test_sequences)

    train_sequences, test_sequences = split_train_and_test(sequences_target_features_ewm, test_rows)
    X_train.append(train_sequences)
    X_test.append(test_sequences)


    X_train, X_test = append_train_and_test_arrays(dict_sequences_others_frecuencies_close, test_rows, X_train, X_test)
    X_train, X_test = append_train_and_test_arrays(dict_sequences_others_frecuencies_features_rolling, test_rows, X_train, X_test)
    X_train, X_test = append_train_and_test_arrays(dict_sequences_others_frecuencies_features_ewm, test_rows, X_train, X_test)


    df_real = get_real_test_values(df_1min, test_rows)

    return X_train, Y_train, X_test, Y_test, scaler_x_test_target, df_real

