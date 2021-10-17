import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class footballNN(nn.Module):
    """Going to pass Batch,Players,2,2"""
    """Flattened into 960 nodes"""

    def __init__(self, num_weekly_features):
        super().__init__()
        self.hidden_size = 80
        self.roster_scan_1 = nn.Linear(20, 20).double()
        self.roster_scan_2 = nn.Linear(640, 320).double() # Don't use these right now
        self.roster_scan_3 = nn.Linear(320,40).double()
        self.lstm = nn.LSTMCell(num_weekly_features, self.hidden_size).double() # LSTM Cell
        self.shrink = nn.Linear(40,40).double()
        self.shrink2 = nn.Linear(40, 20).double()
        self.shrink3 = nn.Linear(20, 10).double()
        self.shrink4 = nn.Linear(10, 4).double()
        self.fc = nn.Linear(4, 1).double()
        self.init_weights()

    def init_weights(self):

        for fc in [self.roster_scan_1, self.roster_scan_2,self.roster_scan_3,
                   self.shrink,self.shrink2,self.shrink3,self.shrink4]:
            nn.init.xavier_normal_(fc.weight, gain=1.0)
            nn.init.constant_(fc.bias, 0.0)
        nn.init.xavier_uniform_(self.lstm.weight_ih, gain=1.0)
        nn.init.xavier_uniform_(self.lstm.weight_hh, gain=1.0)
        nn.init.constant_(self.lstm.bias_ih, 0.0)
        nn.init.constant_(self.lstm.bias_hh, 0.0)
        nn.init.xavier_uniform_(self.fc.weight, gain=1.0)
        nn.init.constant_(self.fc.bias, 0.0)
    
    def forward(self, timeless, game_results=None,num_games=None):
        if game_results is None: # predict first week
            rosters = F.relu(self.roster_scan_1(timeless))
            """rosters = F.relu(self.roster_scan_2(rosters))
            rosters = F.relu(self.roster_scan_3(rosters))
            rosters = F.relu(self.shrink(rosters))
            rosters = F.relu(self.shrink2(rosters))"""
            rosters = F.relu(self.shrink3(rosters))
            rosters = F.sigmoid(self.shrink4(rosters))
            #rosters = rosters.view(-1, self.hidden_size)
            output = self.fc(rosters)

            return output
        else: # predict rest of the weeks
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
