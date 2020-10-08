from src.train.interface_epoch.channel_to_screen.figure.sell_buy_no_actions import SellBuyNoActionsOPerationsFigure
from src.train.interface_epoch.channel_to_screen.print.sell_buy_no_actions import SellBuyNoActionsOPerationsPrint
from src.train.interface_epoch.interface import Interface
from ast import literal_eval

class BasicInterface(Interface):

    
    def __init__(self, source_data, id_cache):

        self._source_data = source_data
        self._channels = {'figure' : SellBuyNoActionsOPerationsFigure(id_cache),
                          'print' : SellBuyNoActionsOPerationsPrint(source_data)}
        self._inputs_channels = {name : self._get_channel_inputs(channel) 
                                 for name, channel in self._channels.items()}

    @property
    def channels(self):
        return self._channels

    @property
    def source_data(self):
        return self._source_data
    
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
                       if name_input in self._input_channels[name]})

    
