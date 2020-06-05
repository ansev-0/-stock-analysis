from keras.layers import Conv1D, Multiply, Add

class CausalWaveBlock:
    
    def __init__(self, filters, kernel_size, n_layers):
        self.tanh_branches = None
        self.sigmoid_branches = None
        self.preprocess_dense = None
        self.outputs_dense = None
        
        self.filters = filters
        self.kernel_size = kernel_size
        self._n_layers = n_layers
        self._dilation_rates = self._get_dilation_rates()
        self._build()
        
    @property
    def dilation_rates(self):
        return self._dilation_rates
        
    @property
    def n_layers(self):
        return self._n_layers
    
    
    def __call__(self, inp, return_skips=True, return_residual=True):
        
        #wavenet
        branches = zip(self.tanh_branches, self.sigmoid_branches, self.outputs_dense)
        x = self.preprocess_dense(inp)
        res_x = x
        skips = []

        for tanh_brach, sigmoid_branch, output_dense in branches:
            
            tanh_result, sigm_result = tanh_brach(x), sigmoid_branch(x)
            x = Multiply()([tanh_result, sigm_result])
            x = output_dense(x)
            res_x = Add()([res_x, x])
            skips.append(x)

        #get params to return 
        output = tuple(param  for param, not_filter
                       in zip((res_x, skips), 
                              (return_residual, return_skips))
                       if not_filter)
        
        #return params
        if len(output)==1:
            return output[0]
        return output


    def _get_dilation_rates(self):
        return (2**i for i in range(self._n_layers))
        
            
    def _build(self):
        self.preprocess_dense = Conv1D(filters=self.filters, kernel_size=1, padding='same')
        self.tanh_branches = self._list_map_dilation_rates(lambda dilation_rate:\
                                                           self._causal_conv1d('tanh',
                                                           dilation_rate))                   
        self.sigmoid_branches = self._list_map_dilation_rates(lambda dilation_rate:\
                                                           self._causal_conv1d('sigmoid',
                                                           dilation_rate))
        self.outputs_dense = self._list_map_dilation_rates(lambda dilation_rate:\
                                                           Conv1D(filters=filters,
                                                                  kernel_size=1, 
                                                                  padding='same'))
        
    def _causal_conv1d(self, activation, dilation_rate):
        return Conv1D(filters=self.filters,
                       kernel_size=self.kernel_size, 
                       padding='causal',
                       activation = activation,
                       dilation_rate=dilation_rate)
    
    def _list_map_dilation_rates(self, function):
        return list(map(function, self._dilation_rates))
