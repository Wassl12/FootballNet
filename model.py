import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class RNN(nn.Module):
    """Going to pass Batch,Players,2,2"""

    def __init__(self, num_weekly_features):
        super().__init__()
        self.hidden_size = 80
        self.roster_scan_1 = nn.Conv2d(240, out_channels=240, kernel_size=1)
        self.roster_scan_2 = nn.Conv2d(240, 80, kernel_size=2)
        self.lstm = nn.LSTMCell(num_weekly_features, self.hidden_size)
        self.fc = nn.Linear(self.hidden_size, 2)
        self.init_weights()

    def init_weights(self):

        for conv in [self.roster_scan_1, self.roster_scan_2]:
            nn.init.xavier_uniform_(conv.weight, gain=1.0)
            nn.init.constant_(conv.bias, 0.0)
        nn.init.xavier_uniform_(self.lstm.weight_ih, gain=1.0)
        nn.init.xavier_uniform_(self.lstm.weight_hh, gain=1.0)
        nn.init.constant_(self.lstm.bias_ih, 0.0)
        nn.init.constant_(self.lstm.bias_hh, 0.0)
        nn.init.xavier_uniform_(self.fc.weight, gain=1.0)
        nn.init.constant_(self.fc.bias, 0.0)
    
    def forward(self, timeless, time):
        batch, channels, width, height = timeless.shape
        rosters = F.sigmoid(self.roster_scan_1(timeless))
        rosters = F.sigmoid(self.roster_scan_2(rosters))
        rosters = rosters.view(-1, self.hidden_size)
        h_t = rosters.clone()
        c_t = rosters.clone()
        output = [self.fc(rosters)]

        batch, num_weekly_features, length = time.shape
        for chunk in time.split(1, dim=1):
            chunk = torch.squeeze(chunk, dim=1)
            h_t, c_t = self.lstm(chunk, (h_t, c_t))
            output.append(self.fc(h_t))

        return output
