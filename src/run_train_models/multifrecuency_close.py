import json
import time
import pandas as pd
import numpy as np
from src.train.admin import admin
from src.data_preparation.multifrecuency_close import generate_train_and_test_data
from src.view.check_results.check_frame import show_predictions_by_days
from src.train.multifrecuency_close import train_model
from src.data_preparation.tools.map.type import history_to_float
from src.validation.dataframe_result import DataFrameAcurracyForecasting
from src.models.keras.seq_to_one.multifrecuency_close import cnn_lstm

FRECUENCY_TARGET = '30T'
OTHERS_FRECUENCIES = ['15T', '10T', '5T', '1T']
TEST_ROWS = 390
str_frecuencies = '_'.join(sorted([FRECUENCY_TARGET] + OTHERS_FRECUENCIES))

def rapid_balance(df_comp):
    
    incr_pred = df_comp['test'].sub(df_comp['real'].shift())
    incr_real = df_comp['real'].diff()
    hit_serie = np.sign(incr_pred) == np.sign(incr_real)
    mean = hit_serie[1:].mean()*100
    print(f'Mean Accuracy: {mean} %')
    balance = incr_real.abs().loc[hit_serie].sum() -incr_real.abs().loc[~hit_serie].sum()
    print('Balance: ', balance)
    return balance, hit_serie, mean

def get_df_comp(df_real, df_test):
    return pd.concat([df_real, df_test], axis=1).set_axis(['real', 'test'], axis=1)


def run():
    
    adminget_orders = admin.DataBaseAdminTrainOrdersGet(train_type='multifrecuency')
    admin_update_results = admin.DataBaseAdminTrainOrdersUpdateResults(train_type='multifrecuency')

    #get first order
    order = adminget_orders.get_first_pending()
    print('Order : \n', order)
    
    while order:
        #reset dict results
        dict_results = {}
        #get order
        company = order['active']
        delays = list(map(int, order['delays']))
        start = order['train_start']
        end = order['train_end']
        id_train = order['_id']
        # show company and delayss of series in tensor
        print(f'Working with company {company}')    
        print(f'Working with {delays} delays')
        
        #data prep
        (X_train, Y_train,
         X_test,_, 
         scaler, df_real) = generate_train_and_test_data(company,
                                                         start,
                                                         end,
                                                         delays,
                                                         OTHERS_FRECUENCIES,
                                                         FRECUENCY_TARGET,
                                                         TEST_ROWS)


        
        print('Data for train obtained')
        print('Shape of test data', Y_train.shape[0])

        #get model
        model = cnn_lstm(8, 12) #### HERE

        name_model = f'30_multifrecuency_cnn_{company}_{delays}_{str_frecuencies}.h5'
        model.name = name_model[:-3]
        #train model
        model, result_1, result_2 = train_model(model=model,
                                                x_train=X_train,
                                                y_train=Y_train,
                                                name_model=name_model,
                                                epochs=250)
        #save result of train
        dict_results['name_model'] = name_model
        dict_results['train_without_val'] = json.dumps(history_to_float(result_2))
        dict_results['train_with_val'] = json.dumps(history_to_float(result_1))
        
        # predictions
        predictions = model.predict(X_test)
        df_pred = np.expm1(pd.DataFrame(scaler.inverse_transform(predictions.squeeze()).T,
                   index=df_real.index, columns=df_real.columns))
        
        #get df_comp
        df_comp = get_df_comp(df_real, df_pred)
        dict_results['df_comp'] = df_comp.to_json()
        
        #show predictions
        show_predictions_by_days(df_comp)
        
        #get balance and hit
        balance, hit_serie, mean = rapid_balance(df_comp)
        dict_results['balance'] = str(balance)
        dict_results['mean_hit'] = str(mean)
        dict_results['hit'] = hit_serie.to_json()
        
        
        #update results and status
        admin_update_results.update_result_and_status(id_train, dict_results)
        
        print('\n' * 50)
        time.sleep(10)

        #get next order
        order = adminget_orders.get_first_pending()
        print('Order : \n', order)

#run()