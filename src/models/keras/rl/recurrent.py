from keras.layers import Dense, Input, LSTM, Conv1D, Concatenate, Dropout, BatchNormalization, Multiply, Flatten, LayerNormalization, TimeDistributed, MaxPool1D
from src.models.keras.tools.wavenet import CausalSimpleWaveBlock
from keras.models import load_model, Model
from keras.optimizers import Adam
from keras.regularizers import L1L2
import tensorflow.keras.backend as K
from keras.layers import Lambda
from tensorflow.keras.constraints import max_norm

def build_dqn(lr, n_actions, 
              input_dims_serie, input_dims_commision, input_dims_portfolio, 
              lstm1_units, lstm2_units, lstm_units_commision, output_fc_dims):

    input_daily_serie = Input(shape = input_dims_serie)
    input_commision = Input(shape = input_dims_commision)
    input_portfolio_status = Input(shape = input_dims_portfolio, name='states_env')

    lstm1_tensor = LSTM(lstm1_units, return_sequences=True, bias_regularizer=L1L2(0.001, 0.001))(input_daily_serie)
    lstm2_tensor = LSTM(lstm2_units, return_sequences=True,bias_regularizer=L1L2(0.001, 0.001))(lstm1_tensor)

    lstm_commision_tensor = LSTM(lstm_units_commision, 
                                 return_sequences=True, 
                                 bias_regularizer=L1L2(0.001, 0.001))(input_commision)

    fc2_portfolio = Conv1D(50, padding ='causal', kernel_size=2, bias_regularizer=L1L2(0.001, 0.001))(input_portfolio_status)

    lstm_portfolio_input = Concatenate(axis=2)([lstm2_tensor, fc2_portfolio, lstm_commision_tensor])
    lstm3_tensor = LSTM(lstm2_units, bias_regularizer=L1L2(0.001, 0.001))(lstm_portfolio_input)

    output_fc = Dense(output_fc_dims, activation = 'relu', bias_regularizer=L1L2(0.001, 0.001))(lstm3_tensor)
    output_fc = Dropout(0.1)(output_fc)
    output = Dense(n_actions, activation = 'linear', bias_regularizer=L1L2(0.001, 0.001))(output_fc)
    output = Dropout(0.1)(output)

    model = Model(inputs = [input_daily_serie, input_commision, input_portfolio_status], outputs=output)
    ## compile model
    model.compile(optimizer=Adam(lr=lr), loss='mse')

    return model



def build_dqn_1(lr, n_actions, 
                input_dims_serie, input_dims_commision, input_dims_portfolio, 
                lstm1_units, lstm2_units, lstm_units_commision, output_fc_dims):

    f = lambda x: K.squeeze(x, axis=1)
    squeeze_f = Lambda(f)

    input_daily_serie = Input(shape = input_dims_serie)
    input_commision = Input(shape = input_dims_commision)
    input_portfolio_status = Input(shape = (1, input_dims_portfolio), name='states_env')
    #
    lstm1_tensor = LSTM(lstm1_units, return_sequences=True, bias_regularizer=L1L2(0.001, 0.001))(input_daily_serie)
    lstm2_tensor = LSTM(lstm2_units, return_sequences=True,bias_regularizer=L1L2(0.001, 0.001))(lstm1_tensor)
    lstm_commision_tensor = LSTM(lstm_units_commision, 
                                 return_sequences=True, 
                                 bias_regularizer=L1L2(0.001, 0.001))(input_commision)
    #
    fc2_portfolio = Conv1D(50, padding = 'causal', kernel_size=2, bias_regularizer=L1L2(0.001, 0.001))(input_portfolio_status)
    fc2_portfolio = squeeze_f(fc2_portfolio)
    #
    lstm_all_input = Concatenate(axis=2)([lstm2_tensor, lstm_commision_tensor])
    lstm3_tensor = LSTM(lstm2_units, bias_regularizer=L1L2(0.001, 0.001))(lstm_all_input)
    #merge
    tensor_2d = Concatenate(axis=1)([lstm3_tensor, fc2_portfolio])

    #output
    output_fc = Dense(output_fc_dims, activation = 'linear', bias_regularizer=L1L2(0.001, 0.001))(tensor_2d)
    output_fc = Dropout(0.1)(output_fc)
    output = Dense(n_actions, activation = 'linear', bias_regularizer=L1L2(0.001, 0.001))(output_fc)
    output = Dropout(0.1)(output)

    model = Model(inputs = [input_daily_serie, input_commision, input_portfolio_status], outputs=output)
    ## compile model
    model.compile(optimizer=Adam(lr=lr), loss='mse')

    return model

def build_dqn_financial(lr, 
                        n_actions, 
                        input_dims_serie, 
                        input_dims_commision, 
                        input_dims_portfolio,
                        input_dims_financial,
                        lstm1_units, 
                        lstm2_units, 
                        lstm_units_commision, 
                        output_fc_dims):
    #squeeze function
    
    squeeze_f = Lambda(lambda x: K.squeeze(x, axis=1))

    input_daily_serie = Input(shape = input_dims_serie)
    input_commision = Input(shape = input_dims_commision)
    input_portfolio_status = Input(shape = (1, input_dims_portfolio), name='states_env')
    input_financial_status = Input(shape = (4, input_dims_financial), name='states_financial')
    #
    #data
    lstm1_tensor = LSTM(lstm1_units, return_sequences=True, bias_regularizer=L1L2(0.001, 0.001))(input_daily_serie)
    lstm2_tensor = LSTM(lstm2_units, bias_regularizer=L1L2(0.001, 0.001))(lstm1_tensor)
    #lstm_2_dense = Dense(150)(lstm2_tensor)

    #commision
    lstm_commision_tensor = LSTM(lstm_units_commision, 
                                 return_sequences=True, 
                                 )(input_commision)
    lstm2_commision_tensor = LSTM(lstm_units_commision,  
                                  )(lstm_commision_tensor)                         
    # env status
    fc2_portfolio_data = squeeze_f(input_portfolio_status)
    fc2_portfolio_data = Dense(50,
                              )(fc2_portfolio_data)
        
    
    ## financial status
    financial_status = LSTM(50, 
                            return_sequences=True, 
                            )(input_financial_status)
    financial_status2 = LSTM(50,  
                             )(financial_status)
    #
    
    

    #fc2_financial_commision = Conv1D(150, padding='causal', kernel_size=1, 
    #                       #bias_regularizer=L1L2(0.001, 0.001)
    #                       )(input_financial_status)
    #fc2_financial_commision = squeeze_f(fc2_financial_commision)
    #
    #lstm_all_input = Concatenate(axis=2)([lstm2_tensor, lstm_commision_tensor])
    # = LSTM(lstm2_units, bias_regularizer=L1L2(0.001, 0.001))(lstm_all_input)
    #merge

    #output_dense_data = Multiply()([lstm_2_dense, fc2_portfolio_data, fc2_financial_data])
    #output_dense_commision = Multiply()([lstm_2_dense, fc2_portfolio_commision, fc2_financial_commision])

    tensor_2d = Concatenate(axis=1)([lstm2_tensor, lstm2_commision_tensor, fc2_portfolio_data, financial_status2])

    #output
    output_fc = Dense(output_fc_dims, activation = 'linear', bias_regularizer=L1L2(0.001, 0.001))(tensor_2d)
    output_fc = Dropout(0.1)(output_fc)
    output = Dense(n_actions, activation = 'linear', bias_regularizer=L1L2(0.001, 0.001))(output_fc)
    output = Dropout(0.1)(output)

    model = Model(inputs = [input_daily_serie, input_commision, input_financial_status, input_portfolio_status], outputs=output)
    ## compile model
    model.compile(optimizer=Adam(lr=lr), loss='mse')

    return model


def build_intraday_dqn_financial(lr, 
                        n_actions, 
                        input_dims_serie, 
                        input_dims_commision, 
                        input_dims_portfolio,
                        input_dims_financial,
                        lstm1_units, 
                        lstm2_units, 
                        lstm_units_commision, 
                        output_fc_dims):
    #squeeze function

    intraday_features = 9
    #wavenet = CausalSimpleWaveBlock(100, 2, 10)



    input_daily_serie = Input(shape = input_dims_serie)
    input_commision = Input(shape = input_dims_commision)
    input_portfolio_status = Input(shape = (input_dims_serie[0], input_dims_portfolio), name='states_env')
    input_financial_status = Input(shape = (4, input_dims_financial), name='states_financial')
    #intraday
    input_intraday_1 = Input(shape = (900, intraday_features), name='intraday_1')
    input_intraday_5 = Input(shape = (512, intraday_features), name='intraday_5')
    input_intraday_30 = Input(shape = (256, intraday_features), name='intraday_30')
    input_intraday_180 = Input(shape = (128, intraday_features), name='intraday_180')

    #data

    #cnn_input_daily = TimeDistributed(MaxPool1D(pool_size=2))(cnn_input_daily)
    #cnn_input_daily = TimeDistributed(Flatten())(cnn_input_daily)
    lstm1_tensor = LSTM(lstm1_units, return_sequences=True)(input_daily_serie)
    lstm2_tensor = LSTM(lstm2_units)(lstm1_tensor)

    #commision
    lstm_commision_tensor = LSTM(lstm_units_commision, 
                                 return_sequences=True)(input_commision)
    lstm2_commision_tensor = LSTM(lstm_units_commision)(lstm_commision_tensor)
    
    # env status
    fc2_portfolio_data = LSTM(50, 
                              return_sequences=True)(input_portfolio_status)
    fc2_portfolio_data = LSTM(50)(fc2_portfolio_data)
    

    output_1min_arr = LSTM(lstm1_units, 
                                 return_sequences=True)(input_intraday_1)
    output_1min = LSTM(lstm2_units)(output_1min_arr)
    

    output_5min_arr = LSTM(lstm1_units, 
                                 return_sequences=True)(input_intraday_5)
    output_5min = LSTM(lstm2_units)(output_5min_arr)


    output_30min_arr = LSTM(lstm1_units, return_sequences=True)(input_intraday_30)
    output_30min = LSTM(lstm2_units)(output_30min_arr)

    output_180min_arr = LSTM(lstm1_units, return_sequences=True)(input_intraday_180)
    output_180min = LSTM(lstm2_units)(output_180min_arr)

    ## financial status

    financial_status = LSTM(50, 
                            return_sequences=True, 
                            )(input_financial_status)
    financial_status2 = LSTM(50,  
                             )(financial_status)
    
    tensor_2d = Concatenate(axis=1)([lstm2_tensor, output_1min, output_5min, output_30min, output_180min, lstm2_commision_tensor, fc2_portfolio_data, financial_status2])
    #output
    dense_all = Dense(1024, activation='relu')(tensor_2d)
    dense_all = Dropout(0.2)(dense_all)
    dense_all = Dense(512, activation='relu')(dense_all)
    output_fc = Dense(output_fc_dims, activation='relu')(dense_all)
    output_fc = Dropout(0.2)(output_fc)
    output = Dense(n_actions, activation = 'linear')(output_fc)

    model = Model(inputs = [input_daily_serie, input_commision, input_financial_status, 
                            input_portfolio_status, input_intraday_1, input_intraday_5, 
                            input_intraday_30, input_intraday_180], outputs=output)
    ## compile model
    model.compile(optimizer=Adam(lr=lr), loss='mse')

    return model