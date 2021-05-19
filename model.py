import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class RNN(nn.Module):
    """Going to pass Batch,Players,2,2"""

    def __init__(self, num_weekly_features):
        super().__init__()
        self.hidden_size = 80
        self.roster_scan_1 = nn.Conv2d(240, out_channels=240, kernel_size=1) # CNN layer
        self.roster_scan_2 = nn.Conv2d(240, 80, kernel_size=2) # CNN Layer
        self.lstm = nn.LSTMCell(num_weekly_features, self.hidden_size) # LSTM Cell
        self.fc = nn.Linear(self.hidden_size, 2) # Create an output from an LSTM Cell
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
    
    def forward(self, timeless, game_results=None,num_games=None):
        if game_results is None: # predict first week
            batch, channels, width, height = timeless.shape # should be b x 240 x 2 x 2
            print("Batch size:",batch)
            print("Channels:", channels)
            print("Width:",width)
            print("Height:",height)
            rosters = F.sigmoid(self.roster_scan_1(timeless))
            rosters = F.sigmoid(self.roster_scan_2(rosters))
            rosters = rosters.view(-1, self.hidden_size)
            output = self.fc(rosters)

            return output
        else: # predict rest of the weeks
            batch, channels, width, height = timeless.shape  # should be b x 240 x 2 x 2
            rosters = F.sigmoid(self.roster_scan_1(timeless))
            rosters = F.sigmoid(self.roster_scan_2(rosters))
            rosters = rosters.view(-1, self.hidden_size)
            h_t = rosters.clone()
            c_t = rosters.clone()
            output = self.fc(rosters)

            batch, num_weekly_features, length = game_results.shape
            for chunk in game_results.split(1, dim=1):
                chunk = torch.squeeze(chunk, dim=1)
                h_t, c_t = self.lstm(chunk, (h_t, c_t))
                output.append(self.fc(h_t))

            return output
