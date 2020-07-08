from keras.layers import Input, RepeatVector
from keras.layers.recurrent import LSTM
from functools import reduce


class BasicLstmToLstm:

    def __init__(self, output_dim, encoder_params, decoder_params, stateful=True):
        self._stateful = stateful
        #init layers
        self.encoder_layer = None
        self.decoder_layer = None
        #get params
        self.output_dim = output_dim
        self.decoder_params = decoder_params
        self.encoder_params = encoder_params

    def __call__(self, tensor_input):
        #create function to get tensor  
        reduce_func = lambda current_tensor, new_layer: new_layer(current_tensor)
        x = tensor_input
        #encoder
        x = reduce(reduce_func, self.encoder_layer, x)
        x = self._repeat_vector(x)
        #decoder
        x = reduce(reduce_func, self.decoder_layer, x)
        return x

    @property
    def stateful(self):
        return self._stateful

    @property
    def output_dim(self):
        return self._output_dim

    @property
    def decoder_params(self):
        return self._decoder_params

    @property
    def encoder_params(self):
        return self._encoder_params

    @output_dim.setter
    def output_dim(self, output_dim):
        self._output_dim = output_dim
        self._update_output_dim()


    @encoder_params.setter
    def encoder_params(self, value):
        self._encoder_params = value
        self._update_encoder_layer()

    @decoder_params.setter
    def decoder_params(self, value):
        self._decoder_params =  value
        self._update_decoder_layer()

#private methods of instance

    def _update_output_dim(self):
        self._repeat_vector = RepeatVector(self._output_dim)


    def _update_encoder_layer(self):
        self.encoder_layer = self._map_list_params(lambda enum_params: \
            LSTM(**dict(enum_params[1], 
                        **{'return_sequences' : enum_params[0] != (len(self._decoder_params) - 1)}),
                 stateful=self._stateful),
                               enumerate(self._encoder_params))
        

    def _update_decoder_layer(self):
       self.decoder_layer = self._map_list_params(lambda params: \
            LSTM(**dict(params,
                        **{'return_sequences' : True}),
                 stateful=self._stateful),
                                                  self._decoder_params)

    @staticmethod
    def _map_list_params(function, list_params):
        return list(map(function, list_params))


