import torch
import torch.nn as nn


class LSTMStateful(nn.Module):
    
    def __init__(self, input_size, hidden_layer_size, batch_size,
                 bidirectional=False, **kwargs):
        
        super().__init__()
        self._hidden_cell = None
        self._batch_size = batch_size
        self._hidden_layer_size = hidden_layer_size
        self._bidirectional = bidirectional
        self.reset_hidden_cell()
        self.lstm = nn.LSTM(input_size, hidden_layer_size,
                            bidirectional=bidirectional, **kwargs)
        
    @property
    def batch_size(self):
        return self._batch_size
        
    @property
    def bidirectional(self):
        return self._bidirectional
        
    @property
    def hidden_layer_size(self):
        return self._hidden_layer_size
    
    @property    
    def hidden_cell(self):
        return self._hidden_cell
    
    def reset_hidden_cell(self):
        self._hidden_cell = (torch.zeros(self.lstm.num_layers * self.bidirectional, 
                                         self.batch_size, self.hidden_layer_size),
                             torch.zeros(self.lstm.num_layers * self.bidirectional,
                                         self.hidden_layer_size))     
        
    def forward(self, input_seq):
        lstm_out, self._hidden_cell = self.lstm(input_seq, self._hidden_cell)
        return lstm_out
