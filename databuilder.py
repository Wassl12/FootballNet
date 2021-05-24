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
    wins_losses = []
    for dict in schedule:
        team1 = dict['home_team']
        team2 = dict['away_team']
        print(team1,team2)
        if team1 in valid_teams or team2 in valid_teams:
            new_schedule.append((team1,team2))
            print(team1,team2)
            try:
                if dict['home_points'] > dict['away_points']:
                    wins_losses.append(0)
                else:
                    wins_losses.append(1)
            except: # the dataset is full of None values, just say the away team won
                wins_losses.append(1)
    print(len(new_schedule))
    print(len(wins_losses))
    return new_schedule, wins_losses# list of tuples (home,away)



if __name__ == "__main__":
    train_brick = []
    validation_brick = []
    validation_labels = []
    train_labels = []
    for year in [2016, 2017, 2018, 2019, 2020]:
        validation_dict = torch.load('tensors/validation{}'.format(year))
        train_dict = torch.load('tensors/train{}'.format(year))
        with open('data/schedules{}.json'.format(year),'r') as schedule:
            schedule_dict = json.load(schedule)
        '''for team, tense in validation_dict.items():
            print(team)
            print(tense[0])'''
        fixed_schedule,wins_losses = schedule_fix(schedule_dict)
        game_num = 0
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
                validation_brick.append({'home_team': home_team, 'away_team': away_team, 'strength': torch.cat((home_brick,away_brick),0)})
                validation_labels.append(wins_losses[game_num])
            else:
                train_brick.append({'home_team': home_team, 'away_team': away_team, 'strength': torch.cat((home_brick,away_brick),0)})
                train_labels.append(wins_losses[game_num])
            game_num += 1
        print(game_num)
        for dict in train_brick: # to help look at actually good teams
            counter = 0
            team_split = 0
            for player in dict['strength']:
                if player[0][0] != 0 or player[0][1] != 0 or player[1][0] != 0 or player[1][1] != 0:
                    counter += 1
                team_split += 1
                if team_split == 120: # other team
                    if counter >= 30:
                        counter = 0
                    else:
                        break
                if team_split == 240:
                    if counter >= 30:
                        print(dict['home_team'])
                        print(dict['away_team'])
    print(len(validation_brick))
    print(len(train_brick))
    print(len(validation_labels))
    print(len(train_labels))
    torch.save(validation_brick,'tensors/validation_data')
    torch.save(train_brick, 'tensors/train_data')
    validation_labels = torch.Tensor(validation_labels)
    train_labels = torch.Tensor(train_labels)
    train_labels_gpu = torch.zeros((len(train_labels)), device=torch.device('cuda'),dtype=torch.long)
    val_labels_gpu = torch.zeros((len(validation_labels)), device=torch.device('cuda'),dtype=torch.long)
    for i in range(len(train_labels)):
        train_labels_gpu[i] = train_labels[i]
    for i in range(len(validation_labels)):
        val_labels_gpu[i] = validation_labels[i]
    torch.save(val_labels_gpu,'tensors/validation_labels')
    torch.save(train_labels_gpu, 'tensors/train_labels')



