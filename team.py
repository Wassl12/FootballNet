import json


class Team():


    def __init__(name,year):
        our__dict = {}
        with open('finalized_rosters{}.json'.format(year)) as f:
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
    

    def clean_info(self,params):
        rating = False
        current_year = False
        with open('ffnn.json') as f:
            info = json.load(f)
        if rating in params:
            rating = True
        if current_year in params:
            current_year = True
        for key, value in info.items():
            for i in range(value):
                try:
                    print(self.roster[key])
                except IndexError:
                    print(name, 'has a small team.')


        