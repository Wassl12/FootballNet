import requests
import json
import os.path
from os import path
cfbd_key = 'VMVOIIRs/yD2q9bmV10VxH8t5ncCPbSwhnelhV+7yos5WNu8OnK5EjC2lFqCwRbc'
def team_fetch():
    if not path.exists('team_list.json'):
        team_list = (requests.get('https://api.collegefootballdata.com/teams')).json()
        teams_clean = {}
        for team in team_list:
            school = team['school']
            teams_clean[school] = {}
            teams_clean[school]['other_names'] = []
            if team['alt_name1'] is not None:
                teams_clean[school]['other_names'].append(team['alt_name1'])
            if team['alt_name2'] is not None:
                teams_clean[school]['other_names'].append(team['alt_name2'])
            if team['alt_name3'] is not None:
                teams_clean[school]['other_names'].append(team['alt_name3'])
        print(teams_clean)
                
        with open('team_list.json', 'w') as fp:
            json.dump(teams_clean, fp)
    else:
        print('Teams already fetched')


def player_creation(current_year):
    """Takes a list of college football teams and fills a roster bases on talent. Needs to be refetched if teams change."""
    if not path.exists('prelim_rosters{}.json'.format(current_year)):
        with open('team_list.json') as f:
            team_list = json.load(f)
        for current_year in [2016,2017,2018,2019,2020,2021]:
            for year in [current_year-5,current_year-4,current_year-3,current_year-2,current_year-1,current_year]: # this needs to fetch current_year-4 as well
                player_list = (requests.get('https://api.collegefootballdata.com/recruiting/players?year={}&classification=HighSchool'.format(year))).json()
                for player in player_list:
                    position = player['position']
                    team_name = player['committedTo']
                    if team_name not in team_list:
                        team_list[team_name] = {}
                    if position not in team_list[team_name]:
                        team_list[team_name][position] = []
                    team_list[team_name][position].append(player)
            with open('prelim_rosters{}.json'.format(current_year), 'w') as fp:
                    json.dump(team_list, fp)
    else:
        print('Preliminary rosters already fetched')
 
def fetch_actual_rosters(current_year):
    """No Dependencies on other data."""
    if not path.exists('verified_rosters{}.json'.format(current_year)):
        for i in range(10):
            verified_rosters = (requests.get('https://api.collegefootballdata.com/roster?year={}'.format(current_year-i))).json()
            with open('verified_rosters{}.json'.format(current_year-i), 'w') as fp:
                json.dump(verified_rosters, fp)
    else:
        print('Actual rosters already fetched')

def fetch_schedules(current_year):
    """No Dependencies on other data."""
    for i in range(10):
        if not path.exists('schedules{}.json'.format(current_year-i)):
            schedules = (requests.get('https://api.collegefootballdata.com/games?year={}&seasonType=regular'.format(current_year-i))).json()
            with open('schedules{}.json'.format(current_year-i), 'w') as fp:
                json.dump(schedules, fp)
    print( 'schedules fetched')

def elo_fetch(years):
    """Years is an array of years you want to search for."""
    for year in years:
        url = "https://api.collegefootballdata.com/ratings/elo?year={}".format(year)
        response = requests.get(url, headers={'Authorization': f'Bearer {cfbd_key}'})
        elos = response.json()
        with open("elos{}.json".format(year),'w') as f:
            json.dump(elos,f)
if __name__ == "__main__":
    #team_fetch()
    #player_creation(2021)
    elo_fetch([2015,2016,2017,2018,2019,2020])
    #fetch_actual_rosters(2020)
    #fetch_schedules(2020)
