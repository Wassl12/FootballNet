import copy

from team import Team
from model import footballNN
import torch.nn
import torch.optim
import json
from torch.nn.functional import softmax
NUM_EPOCHS = 1000
GLOBAL_COUNTER = 0
BATCH_SIZE = 32
SIMULATED_TEAM_SIZE = 19 # Current 18 + elo


def train_step(model, criterion, optimizer, trainX,trainY,valX,valY,val):
    # Tell the model to start training
    m = torch.nn.Sigmoid()
    model.train()

    permutation = torch.randperm(trainX.size()[0])

    # batch size > 1
    if BATCH_SIZE > 1:
        for i in range(0,trainX.size()[0], BATCH_SIZE):
            optimizer.zero_grad()

            indices = permutation[i:i+BATCH_SIZE]
            batch_x, batch_y = trainX[indices], trainY[indices]

            # in case you wanted a semi-full example
            outputs = torch.squeeze(model(batch_x))
            loss = criterion(outputs,batch_y.double())

            loss.backward()
            optimizer.step()
    else:
        for i in range(0, trainX.size()[0]):
            optimizer.zero_grad()

            # in case you wanted a semi-full example
            outputs = torch.squeeze(model(trainX[i]))
            loss = criterion(outputs, trainY[i].double())
            loss.backward()
            optimizer.step()

    # print statistics
    model.eval()
    trainPreds = torch.round(m(torch.squeeze(model(trainX))))
    val_outputs = m(torch.squeeze(model(valX)))
    val_outputs = torch.round(val_outputs)
    print("Train Accuracy:",torch.sum(trainPreds == trainY)/trainY.shape[0])
    print("Validation Accuracy:",torch.sum(val_outputs == valY)/valY.shape[0])
    print("Training loss: ",loss.item())

def main(model,criterion,optimizer):
    train = torch.load('tensors/train_data')
    trainX = train[0]['strength']
    trainX = torch.stack((trainX, train[1]['strength']))
    i = 0
    for game in train:
        if i > 1:
            newGame = torch.unsqueeze(game['strength'], 0)
            trainX = torch.cat((trainX, newGame))
        i += 1

    val = torch.load('tensors/validation_data')
    valX = val[0]['strength']
    valX = torch.stack((valX, val[1]['strength']))
    i = 0
    for game in val:
        if i > 1:
            newGame = torch.unsqueeze(game['strength'], 0)
            valX = torch.cat((valX, newGame))
        i += 1

    valY = torch.load('tensors/validation_labels')
    trainY = torch.load('tensors/train_labels')


    model.to(torch.device('cuda'))

    flattened_train_x = torch.zeros((trainX.shape[0], 2 * SIMULATED_TEAM_SIZE), device=torch.device('cuda'),
                                    dtype=torch.double)
    for i in range(trainX.shape[0]):
        flattened_train_x[i] = torch.flatten(trainX[i])
    trainX = flattened_train_x
    flattened_val_x = torch.zeros((valX.shape[0], 2 * SIMULATED_TEAM_SIZE), device=torch.device('cuda'),
                                  dtype=torch.double)
    for i in range(valX.shape[0]):
        flattened_val_x[i] = torch.flatten(valX[i])
    valX = flattened_val_x

    print("Parameter count", sum(p.numel() for p in model.parameters() if p.requires_grad))
    sig = torch.nn.Sigmoid()
    best_val_accuracy = 0.0
    for epoch in range(NUM_EPOCHS):
        train_step(model, criterion, optimizer, trainX, trainY, valX, valY, val)
        val_outputs = sig(torch.squeeze(model(valX)))
        val_outputs = torch.round(val_outputs)
        val_accuracy = torch.sum(val_outputs == valY) / valY.shape[0]
        if val_accuracy > best_val_accuracy:
            best_val_accuracy = val_accuracy
            print("Copying model...")
            best_model = copy.deepcopy(model)

    torch.save(best_model, 'models/model_{}_{}.pt'.format(sum(p.numel() for p in model.parameters() if p.requires_grad),
                                                          best_val_accuracy))
    val_outputs = sig(torch.squeeze(best_model(valX)))
    print(val_outputs)
    val_outputs = torch.round(val_outputs)
    """for i in range(val_outputs.shape[0]):
        if val[i]['home_team'] == 'Ohio State':
            if val_outputs[i] == 0:
                print("Predicted", 'home', val[i]['home_team'], "over", val[i]['away_team'])
            else:
                print("Predicted", 'away', val[i]['away_team'], "over", val[i]['home_team'])
            if valY[i] == 0:
                print('ACTUAL: ', val[i]['home_team'])
            else:
                print('ACTUAL: ', val[i]['away_team'])
            #print(valX[i])
            print('Quarterback for', val[i]['home_team'], ':',valX[i][0])
            print('Sum for', val[i]['home_team'], ':',sum(valX[i][0:9]))
            print('Quarterback for', val[i]['away_team'], ':', valX[i][10])
            print('Sum for', val[i]['away_team'], ':', sum(valX[i][10:19]))"""
    return  best_model


if __name__ == "__main__":
    criterion = torch.nn.BCEWithLogitsLoss()
    #model = footballNN(0, SIMULATED_TEAM_SIZE)
    model = torch.load("models/model_48365_0.7249283790588379.pt")
    optimizer = torch.optim.SGD(model.parameters(), lr=.0001,momentum=0.9)
    main(model,criterion,optimizer)


