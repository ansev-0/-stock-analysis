from src.train.interface_epoch.channel_to_screen.figure.sell_buy_no_actions import SellBuyNoActionsOPerationsFigure
from src.train.interface_epoch.channel_to_screen.print.sell_buy_no_actions import SellBuyNoActionsOPerationsPrint
from src.train.interface_epoch.channel_to_database.status import TrainAgentStatus
from src.train.interface_epoch.channel_to_database.profit import ProfitEpoch
from src.train.interface_epoch.interface import Interface
from ast import literal_eval
from abc import ABCMeta, abstractproperty

class BasicInterface(Interface):

    def __init__(self, source_data, id_cache, stock_name, train_id):

        #init channels and inputs
        self._channels = {}
        self._inputs_channels = {}
        self._train_id = train_id
        self.id_cache = id_cache
        self.source_data = source_data
        self.stock_name = stock_name

    @property
    def channels(self):
        return self._channels

    @property
    def inputs_channels(self):
        return self._inputs_channels

    @property
    def id_cache(self):
        return self._id_cache

    @id_cache.setter
    def id_cache(self, id_cache):
        self._id_cache = id_cache
        self._channels['figure'] = SellBuyNoActionsOPerationsFigure(id_cache)
        self._inputs_channels['figure'] = self._get_channel_inputs(self._channels['figure'])

    @property
    def train_id(self):
        return self._train_id

    @train_id.setter
    def train_id(self, train_id):
        self._train_id = train_id
        self._channels['status'] = TrainAgentStatus(self._stock_name, train_id)
        self._inputs_channels['status'] = self._get_channel_inputs(self._channels['status'])

    @property
    def stock_name(self):
        return self._stock_name

    @stock_name.setter
    def stock_name(self, stock_name):
        self._stock_name = stock_name
        self._channels['status'] = TrainAgentStatus(stock_name, self._train_id)
        self._inputs_channels['status'] = self._get_channel_inputs(self._channels['status'])
        self._channels['profit'] = ProfitEpoch(self._source_data, self._train_id, self._stock_name)
        self._inputs_channels['profit'] = self._get_channel_inputs(self._channels['profit'])

    @property
    def source_data(self):
        return self._source_data

    @source_data.setter
    def source_data(self, source_data):
        self._source_data = source_data
        self._channels['print'] = SellBuyNoActionsOPerationsPrint(source_data)
        self._inputs_channels['print'] = self._get_channel_inputs(self._channels['print'])

    def get(self, epoch, model, env, states_env, fit_result):
        
        self._check_inputs._is_keras_model(model)
        self._check_inputs._is_env_states(states_env)
        self._check_inputs._is_run_env(env)

        d_inputs = {'epoch' : epoch,
                    'model' : model,
                    'env' : env,
                    'states_env' : states_env,
                    'fit_result' : fit_result}

        for name, channel in self._channels.items():
            channel(**{name_input : inpt 
                       for name_input, inpt in d_inputs.items()
                       if name_input in self._inputs_channels[name]})
