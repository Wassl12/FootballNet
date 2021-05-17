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
    # Local batches and labels
    inputs = []
    labels = []

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
    trainGames = []
    valGames = []

    with open('tensors/train_data') as train:
        for game in train:
            trainGames.append(game['strength'])
    trainX = torch.FloatTensor(trainGames)
    with open('tensors/validation_data') as val:
        for game in val:
            valGames.append(game['strength'])
    valX = torch.FloatTensor(valGames)


    # BATCH SIZE WILL BE THE ENTIRE DATASET
    # IT'S NOT THAT BIG
    # NUM EPOCHS = 20/30/40

    ####################################
    model = RNN(0)
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    ######################################

    print("Parameter count", sum(p.numel() for p in model.parameters() if p.requires_grad))
    for epoch in range(NUM_EPOCHS):
        train_step(model, criterion, optimizer, game_list, validation_dict,train_dict)

