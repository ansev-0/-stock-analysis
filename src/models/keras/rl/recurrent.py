from keras.layers import Dense, Input, LSTM, Conv1D, Concatenate
from keras.models import load_model, Model
from keras.optimizers import Adam


def build_dqn(lr, n_actions, 
              input_dims_serie, input_dims_portfolio, 
              lstm1_units, lstm2_units, output_fc_dims):

    input_daily_serie = Input(shape = input_dims_serie)
    input_portfolio_status = Input(shape = input_dims_portfolio, name='states_env')
    lstm1_tensor = LSTM(lstm1_units, return_sequences=True)(input_daily_serie)
    lstm2_tensor = LSTM(lstm2_units, return_sequences=True)(lstm1_tensor)

    fc2_portfolio = Conv1D(50, padding = 'causal', kernel_size=2)(input_portfolio_status)
    
    lstm_portfolio_input = Concatenate(axis=2)([lstm2_tensor, fc2_portfolio])
    lstm3_tensor = LSTM(lstm2_units)(lstm_portfolio_input)

    output_fc = Dense(output_fc_dims, activation = 'linear')(lstm3_tensor)
    output = Dense(n_actions, activation = 'linear')(output_fc)

    model = Model(inputs = [input_daily_serie, input_portfolio_status], outputs=output)
    ## compile model
    model.compile(optimizer=Adam(lr=lr), loss='mse')

    return model