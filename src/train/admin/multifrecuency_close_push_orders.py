from functools import reduce
from src.train.admin import admin

companies=['AMD', 'NFLX', 'GOOGL',
           'ADSK', 'NVDA', 'AAPL','CSCO'
          ]
delays = [[65, 91, 156, 208 , 260]] * len(companies)
TRAIN_START = '03/01/2020'
TRAIN_END = '04/01/2020'



def push_order(company, delay):

    admin_generator=admin.DataBaseAdminTrainOrdersGeneratorTimeSeriesOptimizer\
    (train_type = 'multifrecuency',
    active=company,
    train_start=TRAIN_START,
    train_end=TRAIN_END,
    delays=delay,
    optimizer_params={'loss' : 'mse',
                     'optimizer' : 'adam'})
    
    orders = admin_generator.push_order()
    return orders


def push_combinations_orders(list_companies, list_delays):
    
    return reduce(lambda cum, new: cum + new, ([push_order(company, delay) 
                                                for delay in delays] 
                                                for company in companies))


combinations = reduce(lambda cum, new: cum + new, ([(company, delay) for delay in delays] 
                                    for company in companies))
                                    
push_combinations_orders(companies, delays)