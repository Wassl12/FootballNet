import requests
import json
import os.path
from os import path


def verify_rosters(current_year):
    with open('verified_rosters{}.json'.format(current_year)) as f:
        verified_roster = json.load(f)
    with open('prelim_rosters{}.json'.format(current_year)) as fp:
        prelim_roster = json.load(fp)
    #I'm not super concerned if players transfer
    #They're GENERALLY not as good as their index says
    final_rosters = {}
    for person in verified_roster:
        try:
            player_name = person['first_name'] + ' ' + person['last_name']
        except:
            #print(person, " is a buggy datapoint")
            continue
        person_team = person['team']
        position = person['position']
        try:
            if detect_player(prelim_roster[person_team][position],player_name):
                if person_team in final_rosters:
                    if position in final_rosters[person_team]:
                        final_rosters[person_team][position].append(person)
                    else:
                        final_rosters[person_team][position] = [person]
                else:
                    final_rosters[person_team] = {position: [person]}
            else:
                pos = sweep_roster(prelim_roster[person_team],player_name)
                if pos is not None:
                    if person_team in final_rosters:
                        if pos in final_rosters[person_team]:
                            final_rosters[person_team][pos].append(person)
                        else:
                            final_rosters[person_team][pos] = [person]
                    else:
                        final_rosters[person_team] = {pos: [person]}


        except KeyError:
            continue
            #print(person_team," has some recruiting problems at ",position)

    print(final_rosters['Michigan']['RB'])
    print(final_rosters['Michigan']['APB'])
    for player in prelim_roster['Michigan']['RB']:
        print(player['name'])
    #RIGHT NOW, the athletes/apb/etc are grouped together but maintain their current position
    #print(prelim_roster['Michigan']['RB'])
    #print(verified_roster['Michigan']['RB'])

    
def detect_player(list_dict,player_name):
    for player in list_dict:
        if player['name'] == player_name:
            return True
    return False

def sweep_roster(team,player_name):
    for key,pos in team.items():
        if key == 'other_names':
            continue
        if detect_player(pos,player_name):
            return key
    return None

if __name__ == "__main__":
    verify_rosters(2020)