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
from src.models.names import NameModel
from src.models.path import PathModel

FRECUENCY_TARGET = '30T'
OTHERS_FRECUENCIES = ['15T', '10T', '5T', '1T']
TEST_ROWS = 390
str_frecuencies = '_'.join(sorted([FRECUENCY_TARGET] + OTHERS_FRECUENCIES))

def rapid_balance(df_comp, shift_n):
    shift_real = df_comp['real'].shift(shift_n)
    notna = shift_real.notna()
    
    incr_pred = df_comp['test'].sub(shift_real)
    incr_real =  df_comp['real'].sub(shift_real)
    
    equals = (np.sign(incr_pred) == np.sign(incr_real))
    
    hit_serie = equals.loc[notna]
    mean = hit_serie.mean()*100
    print(f'Mean Accuracy: {mean} %')
    balance = incr_real.abs().loc[equals & notna].sum() - incr_real.abs().loc[(~equals) & notna].sum()
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


        
        #Get model name
        model_name = NameModel(company, 'close', ['conv1d-lstm-dnn'], 'multifrecuency')()
        #Get path
        path_model = PathModel()(model_name)
        #search model in db
        model = admin.DataBaseAdminTrainOrdersSearchModel(train_type='multifrecuency').get_model(path_model)
        

        if model is None: 
            model = cnn_lstm(8, 12)
        
        #name_model = f'30_multifrecuency_cnn_{company}_{delays}_{str_frecuencies}.h5'

        #train model
        model, result_1, result_2 = train_model(model=model,
                                                x_train=X_train,
                                                y_train=Y_train,
                                                path_model=path_model,
                                                epochs=250)
        #save result of train
        dict_results['path_model'] = path_model
        dict_results['train_without_val'] = json.dumps(history_to_float(result_2))
        dict_results['train_with_val'] = json.dumps(history_to_float(result_1))
        
        # predictions
        predictions = model.predict(X_test)
        df_pred = np.expm1(pd.DataFrame(scaler.inverse_transform(predictions.squeeze()).T,
                   index=df_real.index[-TEST_ROWS:], columns=df_real.columns))
        
        #get df_comp
        df_comp = get_df_comp(df_real, df_pred)
        dict_results['df_comp'] = df_comp.to_json()
        
        #show predictions
        show_predictions_by_days(df_comp, model_name)
        
        #get balance and hit
        balance, hit_serie, mean = rapid_balance(df_comp, 
                                                 int(FRECUENCY_TARGET[:-1])
                                                 )
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