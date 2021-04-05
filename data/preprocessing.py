import requests
import json
import os.path
from os import path
import numpy as np
import sys

def verify_rosters(current_year):
    with open('verified_rosters{}.json'.format(current_year)) as f:
        verified_roster = json.load(f)
    with open('prelim_rosters{}.json'.format(current_year)) as fp:
        prelim_roster = json.load(fp)
    #I'm not super concerned if players transfer
    #They're GENERALLY not as good as their index says
    final_rosters = {}
    positions = {}
    for person in verified_roster:
        try:
            player_name = person['first_name'] + ' ' + person['last_name']
        except:
            #print(person, " is a buggy datapoint")
            continue
        person_team = person['team']
        position = pos_narrow(person['position'])
        if position == '?' or position == None or position == 'ATH':
            continue
        positions[position] = 1
        try:
            if detect_player(prelim_roster[person_team][position],player_name) is not None:
                if person_team in final_rosters:
                    if position in final_rosters[person_team]:
                        final_rosters[person_team][position].append(person)
                    else:
                        final_rosters[person_team][position] = [person]
                else:
                    final_rosters[person_team] = {position: [person]}

                final_rosters[person_team][position][-1]['rating'] = detect_player(prelim_roster[person_team][position],player_name)
            else:
                pos,rating = sweep_roster(prelim_roster[person_team],player_name)
                if position == 'DB':
                    print('DB')
                if position == 'CB':
                    print('CB')
                if pos is not None:
                    pos = position #this will change where players are stored
                    if person_team in final_rosters:
                        if pos in final_rosters[person_team]:
                            final_rosters[person_team][pos].append(person)
                        else:
                            final_rosters[person_team][pos] = [person]
                    else:
                        final_rosters[person_team] = {pos: [person]}
                    final_rosters[person_team][pos][-1]['rating'] = rating


        except KeyError:
            pos,rating = sweep_roster(prelim_roster[person_team],player_name)
            if pos is not None:
                pos = position #this will change where players are stored
                if person_team in final_rosters:
                    if pos in final_rosters[person_team]:
                        final_rosters[person_team][pos].append(person)
                    else:
                        final_rosters[person_team][pos] = [person]
                else:
                    final_rosters[person_team] = {pos: [person]}
                final_rosters[person_team][pos][-1]['rating'] = rating


    print(final_rosters['Michigan']['DB'])
    #print(final_rosters['Michigan']['APB'])
    #for player in prelim_roster['Michigan']['RB']:
        #print(player['name'])
    #RIGHT NOW, the athletes/apb/etc are grouped together but maintain their current position
    #print(prelim_roster['Michigan']['RB'])
    #print(verified_roster['Michigan']['RB'])
    with open('finalized_rosters{}.json'.format(current_year), 'w') as fp:
        json.dump(final_rosters, fp)
    """for key,value in positions.items():
        print(key)"""

    
def detect_player(list_dict,player_name):
    for player in list_dict:
        if player['name'] == player_name:
            return player['rating']
    return None

def sweep_roster(team,player_name):
    for key,pos in team.items():
        if key == 'other_names':
            continue
        if detect_player(pos,player_name) is not None:
            return key, detect_player(pos,player_name)
    return None,None

def pos_narrow(position):
    if position == 'OT' or position == 'LS' or position == 'G' or position == 'C':
        return 'OL'
    if position == 'FB':
        return 'TE'
    if position == 'DE' or position == 'NT' or position == 'DT':
        return 'DL'
    if position == 'CB' or position == 'S':
        return 'DB'
    return position


"""def narrow_roster(current_year)
    with open('finalized_rosters{}.json'.format(current_year)) as f:
        verified_roster = json.load(f)"""
    


if __name__ == "__main__":
    verify_rosters(2020)
