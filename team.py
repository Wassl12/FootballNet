import json
import torch.nn


class Team():

    def __init__(self, name, year):
        our__dict = {}
        with open('data/finalized_rosters{}.json'.format(year)) as f:
            our_dict = json.load(f)
        self.roster = {}
        self.roster['QB'] = our_dict[name]['QB'] # should be a list of quarterbacks
        self.roster['RB'] = our_dict[name]['RB']
        self.roster['OL'] = our_dict[name]['OL']
        self.roster['WR'] = our_dict[name]['WR']
        self.roster['TE'] = our_dict[name]['TE']
        self.roster['DB'] = our_dict[name]['DB']
        self.roster['LB'] = our_dict[name]['LB']
        self.roster['DL'] = our_dict[name]['DL']
        self.roster['PK'] = our_dict[name]['PK']
        self.roster['P'] = our_dict[name]['P']
        self.remove_dupes()
        for pos, players in self.roster.items():
            for play in self.roster[pos]:
                if 'rating' not in play:
                    play['rating'] = 0.7
            players.sort(reverse=True, key=lambda player: player['rating']+player['year']/7)
        self.clean_info({})

    def clean_info(self, params):
        rating = False
        current_year = False
        with open("data/ffnn.json") as f:
            info = json.load(f)
        if rating in params:
            rating = True
        if current_year in params:
            current_year = True
        for key, value in info.items():
            print(key)
            for i in range(value):
                try:
                    print(self.roster[key][i]['first_name'], end=' ')
                    print(self.roster[key][i]['last_name'], end=' ')
                    print(self.roster[key][i]['rating'], end='\n')
                except IndexError:
                    print(' small team.')

    def remove_dupes(self):
        for pos, players in self.roster.items():
            for i in range(len(self.roster[pos])):
                for n in range(i+1,len(self.roster[pos])):
                    if self.roster[pos][i]['id'] == self.roster[pos][n]['id']:
                        self.roster[pos].pop(n)
                        self.remove_dupes()  # extremely lazy
                        return


if __name__ == "__main__":
    print(torch.__version__)
    print(torch.cuda.is_available())
    print(torch.cuda.get_device_name(device=None))
    michigan = Team('Michigan', 2020)
    # michigan.clean_info({'rating': True, 'current_year': 2020})


        