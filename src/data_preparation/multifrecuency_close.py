
import pandas as pd
import numpy as np
from src.read_database.stock_data import StockDataFromDataBase as reader

from pymongo import MongoClient
from src.data_preparation.tools.resample.ohlcv import ResampleOhlcDataFrame
from src.data_preparation.tools.fill_missing_values.bygroups import FillByPeriods
from src.data_preparation.tools.expand.stacked_delay import  StackedSequencesFromSeries
from src.data_preparation.tools.filter.filter_dataframe import  filter_open_market_hours
from src.data_preparation.tools.split.io_dataset_split import SplitIO
from sklearn.preprocessing import StandardScaler




def prepare_dataframe(dataframe, freq, add_cols=None, dataframe_freq='T', delay_tolerance=None):
    
    if freq == dataframe_freq:
        df = dataframe.asfreq(freq).between_time('09:31', '16:00')
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


def generate_train_and_test_data(company,
                                 init_date, 
                                 last_date,
                                 delay, 
                                 frecuencies_features,
                                 frecuency_target,
                                 test_rows):
    
    #get data from database
    df = get_data_from_base(company, init_date, last_date)
    
    #others frecuency sequences
    dict_df_features = {freq : prepare_dataframe(df, freq) for freq in frecuencies_features}
    dict_close_log1p = {freq : np.log1p(dataframe['close']) for freq, dataframe in dict_df_features.items()}
    dict_df_sequences_features = {freq : get_stacked_sequences(serie, delay) 
                                  for freq, serie in dict_close_log1p.items()}

    #sequences target
    target_df = prepare_dataframe(df, frecuency_target)
    sequences_target = get_stacked_sequences(np.log1p(target_df['close']), 
                                             delay,
                                             not_include_target = False)
    
    #cut others frecuencies
    dict_df_sequences_features = {freq : sequences.loc[sequences_target.index] 
                                  for freq, sequences in dict_df_sequences_features.items()}
    

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
    
    #others frecuency sequences scale

    for sequence in dict_df_sequences_features.values():
        sequence_scaled, _ = scale_x_data(sequence)
        train_sequences, test_sequences = split_train_and_test(sequence_scaled, test_rows)
        X_train.append(train_sequences)
        X_test.append(test_sequences)
        
    #real df to comp   
    df_real = get_real_test_values(target_df, test_rows)  
    
    return X_train, Y_train, X_test, Y_test, scaler_x_test_target, df_real

