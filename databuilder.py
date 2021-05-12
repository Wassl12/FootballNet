import json
import torch.nn
from model import RNN

def schedule_fix(schedule):
    """Return a schedule with all FCS only games stripped."""
    valid_teams = {}
    with open('data/fbs.txt', 'r') as fbs:
        for line in fbs:
            line = line.strip('\n')
            print(line[-1])
            valid_teams[line] = True
    new_schedule = []
    for dict in schedule:
        team1 = dict['home_team']
        team2 = dict['away_team']
        print(team1,team2)
        if team1 in valid_teams or team2 in valid_teams:
            new_schedule.append((team1,team2))
    print(new_schedule)
    return new_schedule



if __name__ == "__main__":
    for year in [2016, 2017, 2018, 2019, 2020]:
        validation_dict = torch.load('tensors/validation{}'.format(year))
        train_dict = torch.load('tensors/train{}'.format(year))
        with open('data/schedules{}.json'.format(year),'r') as schedule:
            schedule_dict = json.load(schedule)
        for team, tense in validation_dict.items():
            print(team)
            print(tense[0])
        fixed_schedule = schedule_fix(schedule_dict)
        train_brick = []
        validation_brick = []
        for home_team, away_team in fixed_schedule:
            if home_team in validation_dict:
                home_brick = validation_dict[home_team]
            else:
                home_brick = train_dict[home_team]
            if away_team in validation_dict:
                away_brick = validation_dict[away_team]
            else:
                away_brick = train_dict[away_team]
            if home_team in validation_dict or away_team in validation_dict:
                validation_brick.append(home_brick+away_brick)
            else:
                train_brick.append({'home_team': home_team, 'away_team': away_team, 'strength': home_brick+away_brick})
        for dict in train_brick: # to help look at actually good teams
            print(dict['home_team'])
            print(dict['away_team'])
            counter = 0
            team_split = 0
            for player in dict['strength']:
                if player[0][0] == 0 and player[0][1] == 0 and player[1][0] == 0 and player[1][1] == 0:
                    continue
                else:
                    print(counter)
                    counter += 1
                team_split += 1
                if team_split == 120: # other team
                    if counter >= 30:
                        counter = 0
                    else:
                        break
                if team_split == 240:
                    if counter >= 30:
                        print(dict)
        torch.save(validation_brick,'tensors/validation_data')
        torch.save(train_brick, 'tensors/train_data')



