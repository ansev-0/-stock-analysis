from keras.models import Model
from keras.layers import Input, Dense, Dropout, TimeDistributed, AveragePooling1D, Lambda
from src.models.keras.tools.attention import AttentionDecoder
from src.models.keras.tools.wavenet import CausalWaveBlock, CausalSimpleWaveBlock
from src.models.keras.tools.seqtoseq import BasicLstmToLstm
from keras.regularizers import L1L2
from keras.layers.recurrent import LSTM

class LstmToLstm:

    def __init__(self, 
                 output_dim,
                 units_encoder,
                 units_decoder,
                 output_dim_attention,
                 units_dense=128,
                 dropout_1=0.2,
                 dropout_2=0.2,
                 dropout_3=0.2,
                 bias_regularizer_encoder=None,
                 bias_regularizer_decoder=None):

        self._attention = AttentionDecoder(units_decoder, output_dim_attention)

        self._basic_lstm_to_lstm = BasicLstmToLstm(encoder_params=[{'units' : units_encoder, 
                                         'bias_regularizer' : bias_regularizer_encoder}], 
                                                   decoder_params=[{'units' : units_decoder,
                                         'bias_regularizer' : bias_regularizer_decoder}],
                        output_dim=output_dim,
                        stateful=False)

        self._dense = TimeDistributed(Dense(units_dense, activation="relu"))

        self._dropout_1 = Dropout(dropout_1)
        self._dropout_2 = Dropout(dropout_2)
        self._dropout_3 = Dropout(dropout_3)

    def __call__(self, input_tensor):   
        x = self._basic_lstm_to_lstm(input_tensor)
        x = self._dropout_1(x)
        x = self._attention(x)
        x = self._dropout_2(x)
        x = self._dense(x)
        x = self._dropout_3(x)
        x = TimeDistributed(Dense(1))(x)

        return x


class SimpleWavenet:

    def __init__(self, 
                 output_dim,
                 n_filters,
                 kernel_size=2,
                 n_layers=1,
                 units_dense=128,
                 dropout=0,
                 bias_regularizer=None,
                 kernel_regularizer=None):

        self._causal_simple_wavenet = CausalSimpleWaveBlock(filters=n_filters,
                                                            kernel_size=kernel_size,
                                                            n_layers=n_layers,
                                                            bias_regularizer=bias_regularizer,
                                                            kernel_regularizer=kernel_regularizer)
        self._output_dim = output_dim
        self._dense = TimeDistributed(Dense(units_dense, activation="relu"))
        self._dropout = Dropout(dropout)
        self._slice_layer = Lambda(lambda x, seq_length: x[:,-seq_length:,:] ,
                                   arguments={'seq_length':  self._output_dim})

    @property
    def output_dim(self):
        return self._output_dim

    def __call__(self, input_tensor):

        x = self._causal_simple_wavenet(input_tensor)
        x = self._dense(x)
        x = self._dropout(x)
        x = Dense(1)(x)
        x = self._slice_layer(x)
        return x


    def update_bias_regularizer(self, positions, value):
        for position in positions:
            self._causal_simple_wavenet.update_params(position,
                                                      'bias_regularizer', value)
  
    def update_kernel_regularizer(self, positions, value):
        for position in positions:
            self._causal_simple_wavenet.update_params(position,
                                                      'kernel_regularizer', value)





#######################################################

class WavenetAttention:

    def __init__(self,
                 n_filter_1, 
                 n_filter_2, 
                 n_layers_1,
                 n_layers_2,
                 pool_1,
                 pool_2,
                 units_lstm,
                 output_dim_attention,
                 bias_regularizer_lstm=None,
                 bias_regularizers_tanh_branch_1=None,
                 bias_regularizers_sigmoid_branch_1=None,
                 bias_regularizers_tanh_branch_2=None,
                 bias_regularizers_sigmoid_branch_2=None,
                 units_dense=100,
                 dropout_1=0.2,
                 dropout_2=0.2,
                 dropout_3=0.2):

        self._causal_wave_1 = CausalWaveBlock(n_filter_1, 2, n_layers_1, 
                                              tanh_bias_regularizer=bias_regularizers_tanh_branch_1,
                                              sigmoid_bias_regularizer=bias_regularizers_sigmoid_branch_1)

        self._causal_wave_2 = CausalWaveBlock(n_filter_2, 2, n_layers_2,
                                              tanh_bias_regularizer=bias_regularizers_tanh_branch_2,
                                              sigmoid_bias_regularizer=bias_regularizers_sigmoid_branch_2)


        self._pool_1 = AveragePooling1D(pool_1)
        self._pool_2 = AveragePooling1D(pool_2)

        self._lstm = LSTM(units_lstm, 
                          return_sequences=True, 
                          bias_regularizer = bias_regularizer_lstm)
        
        self._attention = AttentionDecoder(units_lstm, output_dim_attention)

        self._dense = TimeDistributed(Dense(units_dense, activation="relu"))
        self._dropout_1 = Dropout(dropout_1)
        self._dropout_2 = Dropout(dropout_2)
        self._dropout_3 = Dropout(dropout_3)


    def __call__(self, input_tensor):   

        x = self._causal_wave_1(input_tensor, return_skips=False)
        x = self._pool_1(x)
        x = self._causal_wave_2(x, return_skips=False)
        x = self._pool_2(x)
        x = self._lstm(x)
        x = self._dropout_1(x)
        x = self._attention(x)
        x = self._dropout_2(x)
        x = self._dense(x)
        x = self._dropout_3(x)
        x = Dense(1)(x)
        return x

def update_bias_regularizer_tanh_1(self, positions, value):
    for position in positions:
        self._causal_wave_1.update_tanh_params(position,
                                               'bias_regularizer', value)

def update_bias_regularizer_sigmoid_1(self, wave_block, positions, value):
    for position in positions:
        self._causal_wave_1.update_sigmoid_params(position,
                                                  'bias_regularizer', value)

def update_bias_regularizer_tanh_2(self, wave_block, positions, value):
    for position in positions:
        self._causal_wave_2.update_tanh_params(position,
                                               'bias_regularizer', value)

def update_bias_regularizer_sigmoid_2(self, positions, value):
    for position in positions:
        self._causal_wave_2.update_sigmoid_params(position,
                                                  'bias_regularizer', value)





