from keras.layers import Dense, Input, LSTM, Conv1D, Concatenate, Dropout
from keras.models import load_model, Model
from keras.optimizers import Adam
from keras.regularizers import L1L2
import tensorflow.keras.backend as K
from keras.layers import Lambda

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

    fc2_portfolio = Conv1D(50, padding = 'causal', kernel_size=2, bias_regularizer=L1L2(0.001, 0.001))(input_portfolio_status)

    lstm_portfolio_input = Concatenate(axis=2)([lstm2_tensor, fc2_portfolio, lstm_commision_tensor])
    lstm3_tensor = LSTM(lstm2_units, bias_regularizer=L1L2(0.001, 0.001))(lstm_portfolio_input)

    output_fc = Dense(output_fc_dims, activation = 'linear', bias_regularizer=L1L2(0.001, 0.001))(lstm3_tensor)
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
    f = lambda x: K.squeeze(x, axis=1)
    squeeze_f = Lambda(f)

    input_daily_serie = Input(shape = input_dims_serie)
    input_commision = Input(shape = input_dims_commision)
    input_portfolio_status = Input(shape = (1, input_dims_portfolio), name='states_env')
    input_financial_status = Input(shape = (1, input_dims_financial), name='states_financial')
    #
    lstm1_tensor = LSTM(lstm1_units, return_sequences=True, bias_regularizer=L1L2(0.001, 0.001))(input_daily_serie)
    lstm2_tensor = LSTM(lstm2_units, return_sequences=True, bias_regularizer=L1L2(0.001, 0.001))(lstm1_tensor)
    lstm_commision_tensor = LSTM(lstm_units_commision, 
                                 return_sequences=True, 
                                 bias_regularizer=L1L2(0.001, 0.001))(input_commision)
    # env status
    fc2_portfolio = Conv1D(50, padding = 'causal', kernel_size=2, bias_regularizer=L1L2(0.001, 0.001))(input_portfolio_status)
    fc2_portfolio = squeeze_f(fc2_portfolio)
    # financial status
    fc2_financial = Conv1D(150, padding = 'causal', kernel_size=2, bias_regularizer=L1L2(0.001, 0.001))(input_financial_status)
    fc2_financial = squeeze_f(fc2_financial)
    #
    lstm_all_input = Concatenate(axis=2)([lstm2_tensor, lstm_commision_tensor])
    lstm3_tensor = LSTM(lstm2_units, bias_regularizer=L1L2(0.001, 0.001))(lstm_all_input)
    #merge
    tensor_2d = Concatenate(axis=1)([lstm3_tensor, fc2_portfolio, fc2_financial])

    #output
    output_fc = Dense(output_fc_dims, activation = 'linear', bias_regularizer=L1L2(0.001, 0.001))(tensor_2d)
    output_fc = Dropout(0.1)(output_fc)
    output = Dense(n_actions, activation = 'linear', bias_regularizer=L1L2(0.001, 0.001))(output_fc)
    output = Dropout(0.1)(output)

    model = Model(inputs = [input_daily_serie, input_commision, input_financial_status, input_portfolio_status], outputs=output)
    ## compile model
    model.compile(optimizer=Adam(lr=lr), loss='mse')

    return model