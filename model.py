import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class RNN(nn.Module):
    def __init__(self, input_size, 2*roster_size, output_size):
        super().__init__()
        #TODO: fill in the definitions for each layer
        self.hidden_size = hidden_size
        self.lstm = nn.LSTMCell(input_size, hidden_size)
        self.fc = nn.Linear(hidden_size,output_size)
        self.init_weights()

    def init_weights(self):
        #TODO: initialize weights and biases of lstm cells according to specified distributions
        nn.init.xavier_uniform_(self.lstm.weight_ih, gain=1.0)
        nn.init.xavier_uniform_(self.lstm.weight_hh, gain=1.0)
        nn.init.constant_(self.lstm.bias_ih, 0.0)
        nn.init.constant_(self.lstm.bias_hh, 0.0)
        ##
        #TODO: initialize weights and biases of FC layer according to specified distributions
        fc = self.fc
        nn.init.xavier_uniform_(fc.weight, gain=1.0)
        nn.init.constant_(fc.bias, 0.0)
    
    def forward(self, x):
        N, T, d = x.shape
        h_t, c_t = self.init_hidden(N)
        for chunk in x.split(1,dim=1):
            chunk = torch.squeeze(chunk,dim=1)
            h_t, c_t = self.lstm(chunk,(h_t,c_t))



        z = self.fc(h_t)
        z = F.sigmoid(z)
        return z