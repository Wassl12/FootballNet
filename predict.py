from team import Team
from model import RNN
import torch.nn
import torch.optim
import json
NUM_EPOCHS = 20
GLOBAL_COUNTER = 0
BATCH_SIZE = 16


def train_step(model, criterion, optimizer, game_list, validation_dict,train_dict):
    model.train()
    running_loss = 0.0
    for i in range(16):
        # Local batches and labels
        inputs = []
        labels = []

        train

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        print(loss.item())


print('Finished Training')



if __name__ == "__main__":
    game_list = []
    with open('data/schedules2020.json') as games:
        game_son = json.load(games)

    # gathered all of the week 1 games so far
    for game in game_list:
        if game['week'] != 1:
            break
        game_list.append([game['home_team'],game['away_team']])

    model = RNN(0)
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    print("Parameter count", sum(p.numel() for p in model.parameters() if p.requires_grad))
    X , y = torch.load('timeless.pt')
    validation_dict = torch.load('tensors/validation{}'.format(2020))
    train_dict = torch.load('tensors/train{}'.format(2020))
    for epoch in range(NUM_EPOCHS):
        train_step(model, criterion, optimizer, game_list, validation_dict,train_dict)

