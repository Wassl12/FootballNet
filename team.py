import json
import torch.nn
from model import footballNN
SIMULATED_TEAM_SIZE = 18
class Team():

    def __init__(self, name, year,gpu):
        our__dict = {}
        with open('data/finalized_rosters{}.json'.format(year)) as f:
            our_dict = json.load(f)
        self.year = year
        self.name = name
        self.gpu = gpu
        self.roster = {}
        self.layers = []
        try:
            self.roster['QB'] = our_dict[name]['QB']  # should be a list of quarterbacks
        except:
            #print(name, ' has no quarterbacks')
            pass
        try:
            self.roster['RB'] = our_dict[name]['RB']
        except:
            #print(name, ' has no running backs')
            pass
        try:
            self.roster['OL'] = our_dict[name]['OL']
        except:
            #print(name, ' has no offensive linemen')
            pass
        try:
            self.roster['WR'] = our_dict[name]['WR']
        except:
            #print(name, ' has no receivers')
            pass
        try:
            self.roster['TE'] = our_dict[name]['TE']
        except:
            #print(name, ' has no tight ends')
            pass
        try:
            self.roster['DB'] = our_dict[name]['DB']
        except:
            #print(name, ' has no defensive backs')
            pass
        try:
            self.roster['LB'] = our_dict[name]['LB']
        except:
            #print(name, 'has no linebackers')
            pass
        try:
            self.roster['DL'] = our_dict[name]['DL']
        except:
            #print(name, 'has no defensive linemen')
            pass
        try:
            self.roster['PK'] = our_dict[name]['PK']
        except:
            #print(name, ' has no placekickers')
            pass
        try:
            self.roster['P'] = our_dict[name]['P']
        except:
            #print(name, ' has no punters')
            pass

        self.remove_dupes()
        for pos, players in self.roster.items():
            for play in self.roster[pos]:
                if 'rating' not in play or play['rating'] is None:
                    play['rating'] = 0.7
                if 'weight' not in play or play['weight'] is None:
                    play['weight'] = 160
                if 'height' not in play or play['height'] is None:
                    play['height'] = 70
                if 'year' not in play or play['year'] is None:
                    play['year'] = 1
            players.sort(reverse=True, key=lambda player: player['rating'])
        self.create_layers()

    def print_clean_info(self, params):
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

    def create_layers(self):
        # Make the layers tensor a 120(20?)x2x2 image
        self.layers = torch.zeros(SIMULATED_TEAM_SIZE, dtype=float,device=self.gpu)
        global_counter = 0
        with open("data/ffnn.json") as f:
            info = json.load(f)
        for position, occurrences in info.items():
            #print(position, occurrences)
            for i in range(occurrences):
                try:
                    #print(self.roster[position][i]['first_name'], end=' ')
                    #print(self.roster[position][i]['last_name'], end=' ')
                    #print(self.roster[position][i]['rating'], end='\n')
                    self.layers[global_counter+i] = self.roster[position][i]['rating']
                    print(self.roster[position][i]['rating'])
                    #self.layers[global_counter+i][0][0] = self.roster[position][i]['rating']
                    #self.layers[global_counter + i][0][1] = self.roster[position][i]['year']
                    #self.layers[global_counter + i][1][0] = self.roster[position][i]['weight']
                    #self.layers[global_counter + i][1][1] = self.roster[position][i]['height']

                except:
                    """for n in range(i,occurrences*3): # fill in the rest of the guys with dummies
                        self.layers[global_counter + n][0][0] = 0.7
                        self.layers[global_counter + n][0][1] = 1
                        self.layers[global_counter + n][1][0] = 160
                        self.layers[global_counter + n][1][1] = 70"""
                    self.layers[global_counter + i] = 0.7
                    break
            global_counter += occurrences # used to be three but then had problems
        """if self.name == 'Michigan':
            print(self.layers)
            print(self.roster)"""



if __name__ == "__main__":
    cuda = torch.device('cuda')
    print(torch.__version__)
    print(torch.cuda.get_device_name(device=None))
    for year in [2016,2017,2018,2019,2020]:
        validation_split = {}
        train_dict = {}
        validation_dict = {}
        with open('data/hand_picked.json') as val:
            validation_split = json.load(val)
        timeless_dict = {}
        teams = {}
        with open('data/team_list.json') as teams:
            teams = json.load(teams)
        for team, names in teams.items():
            current_team = Team(team, year, gpu=cuda)

            timeless_dict[team] = current_team.layers
        for team in timeless_dict:
            if team in validation_split:
                if team == 'Northwestern':
                    print(timeless_dict[team])
                validation_dict[team] = timeless_dict[team]
            else:
                train_dict[team] = timeless_dict[team]
        torch.save(validation_dict, 'tensors/validation{}'.format(year))
        torch.save(train_dict, 'tensors/train{}'.format(year))




        