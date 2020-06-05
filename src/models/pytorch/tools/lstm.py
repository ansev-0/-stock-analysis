import torch
import torch.nn as nn
from  torch.autograd  import  Variable

class LSTMStateful(nn.Module):
    
    def __init__(self, input_size, hidden_size, batch_size,
                 bidirectional=False, **kwargs):
        
        super().__init__()
        self._hidden_state, self._hidden_cell = (None, None)
        self._batch_size = batch_size
        self._hidden_size = hidden_size
        self._bidirectional = bidirectional
        self.lstm = nn.LSTM(input_size, hidden_size,
                            bidirectional=bidirectional, **kwargs)
        self.reset_hidden_cell()
        self.reset_hidden_state()
        
    @property
    def batch_size(self):
        return self._batch_size
        
    @property
    def bidirectional(self):
        return self._bidirectional
        
    @property
    def hidden_size(self):
        return self._hidden_size
    
    @property    
    def hidden_cell(self):
        return self._hidden_cell
    
    @property    
    def hidden_state(self):
        return self._hidden_state
    
    def reset_hidden_cell(self):

        self._hidden_cell = Variable(torch.zeros(self.lstm.num_layers * (self.bidirectional + 1), 
                                                 self.batch_size, self.hidden_size))

        
    def reset_hidden_state(self):
        self._hidden_state = Variable(torch.zeros(self.lstm.num_layers * (self.bidirectional + 1), 
                                                  self.batch_size, self.hidden_size))   


    def detach_hidden_cell(self):

        self._hidden_cell = self._hidden_cell.detach()

        
    def detach_hidden_state(self):
        self._hidden_state = self._hidden_state.detach()
        
    def forward(self, input_seq):
        lstm_out, (self._hidden_cell, self._hidden_state) = self.lstm(input_seq, 
                                                                      (self._hidden_cell, self._hidden_state))
        return lstm_out, (self._hidden_cell, self._hidden_state)
