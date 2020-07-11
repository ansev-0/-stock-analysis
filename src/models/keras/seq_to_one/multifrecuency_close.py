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