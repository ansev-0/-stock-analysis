from src.train.orders.request.agents.q_learning.tasks_for_request.data_task import DataTask
from src.train.orders.request.agents.q_learning.tasks_for_request.stock_data_intraday.get_data import GetDataTask
from src.train.orders.request.agents.q_learning.tasks_for_request.transform_data import TransformDataIntraday
from pandas import to_datetime
import numpy as np

class StockDataTaskIntraday(DataTask):

    features = ('open', 'high', 'low', 'close', 'volume')
    data_from_db = GetDataTask()
    _default_mbed_conf = {'embed_dim' : 1025, 'step' : 1440, 'lag' : 1}

    def __init__(self, mbed_conf=None, *args,**kwargs):

        self.mbed_conf = mbed_conf if mbed_conf is not None else self._default_mbed_conf
        super().__init__(*args, **kwargs)

    def __call__(self, stock_name, shape_0_train, shape_0_val, index_train=None, index_val=None):

        return tuple(map(lambda conf: self._to_cache(
                self._data_preparation(stock_name, 
                                       *conf)), 
                         ((shape_0_train, index_train), (shape_0_val, index_val))
                        )
        )
    def _get_features(self, df):
        return df.assign(weekday=df.index.weekday, 
                         dayofyear=df.index.dayofyear,
                         hour=df.index.hour,
                         minute=df.index.minute)\
            .loc[:, ('weekday', 'dayofyear', 'hour', 'minute') + self.features]

    def _data_preparation(self, stock_name, shape_0, index):
        #get data
        data = self.data_from_db(stock_name, index)
        #get_features
        data = self._get_features(data)
        transform_features = TransformDataIntraday(self.mbed_conf)
        sequences = transform_features(data)[-shape_0:].astype(np.float32)
        print('intraday', sequences[0, [-3, -2, -1], -2])
        array = np.diff(sequences, axis=1).astype(np.float32)
        assert array.shape[0] == shape_0
        
        return array

    @classmethod
    def delay900lag1(cls, *args, **kwargs):
        return cls({'embed_dim' : 901, 'step' : 1440, 'lag' : 1})

    @classmethod
    def delay512lag5(cls, *args, **kwargs):
        return cls({'embed_dim' : 513, 'step' : 1440, 'lag' : 5})

    @classmethod
    def delay256lag30(cls, *args, **kwargs):
        return cls({'embed_dim' : 257, 'step' : 1440, 'lag' : 30})

    @classmethod
    def delay128lag180(cls, *args, **kwargs):
        return cls({'embed_dim' : 129, 'step' : 1440, 'lag' : 180})
