from team import Team
from model import RNN
import torch.nn
import torch.optim
import json
NUM_EPOCHS = 20
GLOBAL_COUNTER = 0
BATCH_SIZE = 16


def train_step(model, criterion, optimizer, trainX,trainY):
    # Tell the model to start training
    model.train()

    # zero the parameter gradients
    optimizer.zero_grad()

    # forward + backward + optimize
    outputs = model(trainX)
    loss = criterion(outputs, trainY)
    loss.backward()
    optimizer.step()

    # print statistics
    print(loss.item())


print('Finished Training')



if __name__ == "__main__":

    train = torch.load('tensors/train_data')
    trainX = train[0]['strength']
    trainX = torch.stack((trainX,train[1]['strength']))
    i = 0
    for game in train:
        print(game['home_team'])
        print(game['away_team'])
        if i > 1:
            newGame = torch.unsqueeze(game['strength'],0)
            trainX = torch.cat((trainX,newGame))
        i += 1

    val = torch.load('tensors/validation_data')
    valX = val[0]['strength']
    valX = torch.stack((valX,val[1]['strength']))
    i = 0
    for game in val:
        if i > 1:
            newGame = torch.unsqueeze(game['strength'], 0)
            valX = torch.cat((valX,newGame))
        i += 1

    # I don't know a fantastic way to do this
    valY = torch.load('tensors/validation_labels')
    trainY = torch.load('tensors/train_labels')
    valY = torch.Tensor(valY)
    trainY = torch.Tensor(trainY)

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
        print(trainX.shape)
        train_step(model, criterion, optimizer, trainX, trainY)

