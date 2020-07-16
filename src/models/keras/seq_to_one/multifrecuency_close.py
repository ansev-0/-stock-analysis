from keras.models import Model
from keras.layers import Input, Conv1D, Dense, Dropout, Concatenate
from keras.layers.recurrent import LSTM  
from keras.regularizers import L1L2  

def stacked_lstm(delays):
    
    #define input
    tensor_input_30min = Input(shape=(delays, 1))
    tensor_input_15min = Input(shape=(delays, 1))
    tensor_input_10min = Input(shape=(delays, 1))
    tensor_input_5min = Input(shape=(delays, 1))
    tensor_input_1min = Input(shape=(delays, 1))
    
    #stacked lstm layers
    x = LSTM(units=100, return_sequences=True, 
             bias_regularizer=L1L2(0.015, 0.015), 
             kernel_regularizer=L1L2(0.000015, 0.000015)
            )(tensor_input_30min)
    x = LSTM(units=100, 
             bias_regularizer=L1L2(0.015, 0.015),
            kernel_regularizer=L1L2(0.000015, 0.000015)
            )(x)
    
    output_30min = Dense(128)(x)
    output_30min = Dropout(.2)(output_30min)
    
    #stacked lstm layers
    x = LSTM(units=100, return_sequences=True, 
             bias_regularizer=L1L2(0.015, 0.015), 
             kernel_regularizer=L1L2(0.000015, 0.000015)
            )(tensor_input_15min)
    x = LSTM(units=100, 
             bias_regularizer=L1L2(0.015, 0.015),
            kernel_regularizer=L1L2(0.000015, 0.000015)
            )(x)
    
    output_15min = Dense(128)(x)
    output_15min = Dropout(.2)(output_15min)
    
    #stacked lstm layers
    x = LSTM(units=100, return_sequences=True, 
             bias_regularizer=L1L2(0.007, 0.007), 
             kernel_regularizer=L1L2(0.000007, 0.000007)
            )(tensor_input_10min)
    x = LSTM(units=100, 
             bias_regularizer=L1L2(0.007, 0.007), 
             kernel_regularizer=L1L2(0.000007, 0.000007)
            )(x)
    
    output_10min = Dense(128)(x)
    output_10min = Dropout(.2)(output_10min)
    
    #stacked lstm layers
    x = LSTM(units=100, return_sequences=True, 
             bias_regularizer=L1L2(0.007, 0.007), 
             kernel_regularizer=L1L2(0.000007, 0.000007)
            )(tensor_input_5min)
    x = LSTM(units=100, 
             bias_regularizer=L1L2(0.007, 0.007), 
             kernel_regularizer=L1L2(0.000007, 0.000007)
            )(x)
    
    output_5min = Dense(128)(x)
    output_5min = Dropout(.2)(output_5min)
    
    #stacked lstm layers
    x = LSTM(units=100, return_sequences=True, 
             bias_regularizer=L1L2(0.007, 0.007), 
             kernel_regularizer=L1L2(0.000007, 0.000007)
            )(tensor_input_1min)
    x = LSTM(units=100, 
             bias_regularizer=L1L2(0.007, 0.007), 
             kernel_regularizer=L1L2(0.000007, 0.000007)
            )(x)
    
    output_1min = Dense(128)(x)
    output_1min = Dropout(.2)(output_1min)
    
    output = Concatenate()([output_30min, output_15min ,output_10min, output_5min, output_1min])
    
    output = Dense(128)(output)
    output = Dropout(.2)(output)
    output = Dense(1)(output)

    # Building the model
    model = Model([tensor_input_30min, 
                   tensor_input_15min, 
                   tensor_input_10min,
                   tensor_input_5min,
                   tensor_input_1min],
                  output)
    
    return model



def cnn_lstm(rolling_features, ewm_features):
    
    #define input
    tensor_input_30min = Input(shape=(None, 1))
    tensor_input_30min_rolling = Input(shape=(None, rolling_features))
    tensor_input_30min_ewm = Input(shape=(None, ewm_features))

    tensor_input_15min = Input(shape=(None, 1))
    tensor_input_10min = Input(shape=(None, 1))
    tensor_input_5min = Input(shape=(None, 1))
    tensor_input_1min = Input(shape=(None, 1))



    tensor_input_15min_rolling = Input(shape=(None, rolling_features))
    tensor_input_10min_rolling = Input(shape=(None, rolling_features))
    tensor_input_5min_rolling = Input(shape=(None, rolling_features))
    tensor_input_1min_rolling = Input(shape=(None, rolling_features))

    tensor_input_15min_ewm = Input(shape=(None, ewm_features))
    tensor_input_10min_ewm = Input(shape=(None, ewm_features))
    tensor_input_5min_ewm = Input(shape=(None, ewm_features))
    tensor_input_1min_ewm = Input(shape=(None, ewm_features))


    #cnn features

    tensor_cnn_30min = Concatenate()([tensor_input_30min, tensor_input_30min_rolling, tensor_input_30min_ewm])
    cnn_30min = Conv1D(50, padding='causal', kernel_size=2)(tensor_cnn_30min)

    tensor_cnn_15min = Concatenate()([tensor_input_15min, tensor_input_15min_rolling, tensor_input_15min_ewm])
    cnn_15min = Conv1D(50, padding='causal', kernel_size=2)(tensor_cnn_15min)

    tensor_cnn_10min = Concatenate()([tensor_input_10min, tensor_input_10min_rolling, tensor_input_10min_ewm])
    cnn_10min = Conv1D(50, padding='causal', kernel_size=3)(tensor_cnn_10min)

    tensor_cnn_5min = Concatenate()([tensor_input_5min, tensor_input_5min_rolling, tensor_input_5min_ewm])
    cnn_5min = Conv1D(50, padding='causal', kernel_size=6)(tensor_cnn_5min)

    tensor_cnn_1min = Concatenate()([tensor_input_1min, tensor_input_1min_rolling, tensor_input_1min_ewm])
    cnn_1min = Conv1D(50, padding='causal', kernel_size=30)(tensor_cnn_1min)

    input_lstm_30min = Concatenate()([tensor_cnn_30min, cnn_30min])
    input_lstm_15min = Concatenate()([tensor_cnn_15min, cnn_15min])
    input_lstm_10min = Concatenate()([tensor_cnn_10min, cnn_10min])
    input_lstm_5min = Concatenate()([tensor_cnn_5min, cnn_5min])
    input_lstm_1min = Concatenate()([tensor_cnn_1min, cnn_1min])


    #stacked lstm layers
    x = LSTM(units=100, return_sequences=True, 
             bias_regularizer=L1L2(0.015, 0.015), 
             kernel_regularizer=L1L2(0.000015, 0.000015)
            )(input_lstm_30min)
    x = LSTM(units=100, 
             bias_regularizer=L1L2(0.015, 0.015),
            kernel_regularizer=L1L2(0.000015, 0.000015)
            )(x)
    
    output_30min = Dense(128)(x)
    output_30min = Dropout(.2)(output_30min)
    
    #stacked lstm layers
    x = LSTM(units=100, return_sequences=True, 
             bias_regularizer=L1L2(0.015, 0.015), 
             kernel_regularizer=L1L2(0.000015, 0.000015)
            )(input_lstm_15min)
    x = LSTM(units=100, 
             bias_regularizer=L1L2(0.015, 0.015),
            kernel_regularizer=L1L2(0.000015, 0.000015)
            )(x)
    
    output_15min = Dense(128)(x)
    output_15min = Dropout(.2)(output_15min)
    
    #stacked lstm layers
    x = LSTM(units=100, return_sequences=True, 
             bias_regularizer=L1L2(0.007, 0.007), 
             kernel_regularizer=L1L2(0.000007, 0.000007)
            )(input_lstm_10min)
    x = LSTM(units=100, 
             bias_regularizer=L1L2(0.007, 0.007), 
             kernel_regularizer=L1L2(0.000007, 0.000007)
            )(x)
    
    output_10min = Dense(128)(x)
    output_10min = Dropout(.2)(output_10min)
    
    #stacked lstm layers
    x = LSTM(units=100, return_sequences=True, 
             bias_regularizer=L1L2(0.007, 0.007), 
             kernel_regularizer=L1L2(0.000007, 0.000007)
            )(input_lstm_5min)
    x = LSTM(units=100, 
             bias_regularizer=L1L2(0.007, 0.007), 
             kernel_regularizer=L1L2(0.000007, 0.000007)
            )(x)
    
    output_5min = Dense(128)(x)
    output_5min = Dropout(.2)(output_5min)
    
    #stacked lstm layers
    x = LSTM(units=100, return_sequences=True, 
             bias_regularizer=L1L2(0.007, 0.007), 
             kernel_regularizer=L1L2(0.000007, 0.000007)
            )(input_lstm_1min)
    x = LSTM(units=100, 
             bias_regularizer=L1L2(0.007, 0.007), 
             kernel_regularizer=L1L2(0.000007, 0.000007)
            )(x)
    
    output_1min = Dense(128)(x)
    output_1min = Dropout(.2)(output_1min)
    
    output = Concatenate()([output_30min, output_15min ,output_10min, output_5min, output_1min])
    
    output = Dense(128)(output)
    output = Dropout(.2)(output)
    output = Dense(1)(output)

    # Building the model
    model = Model([tensor_input_30min,
                   tensor_input_30min_rolling,
                   tensor_input_30min_ewm,
                   tensor_input_15min, 
                   tensor_input_10min,
                   tensor_input_5min,
                   tensor_input_1min,
                   tensor_input_15min_rolling,
                   tensor_input_10min_rolling,
                   tensor_input_5min_rolling, 
                   tensor_input_1min_rolling,
                   tensor_input_15min_ewm,
                   tensor_input_10min_ewm,
                   tensor_input_5min_ewm, 
                   tensor_input_1min_ewm],
                  output)
    
    return model