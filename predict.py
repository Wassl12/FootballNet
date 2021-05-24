from team import Team
from model import footballNN
import torch.nn
import torch.optim
import json
from torch.nn.functional import softmax
NUM_EPOCHS = 20
GLOBAL_COUNTER = 0
BATCH_SIZE = 16


def train_step(model, criterion, optimizer, trainX,trainY,valX,valY,val):
    # Tell the model to start training
    model.train()

    # zero the parameter gradients
    optimizer.zero_grad()

    # forward + backward + optimize
    outputs = model(trainX)
    print(outputs.shape)
    print(trainY.shape)
    loss = criterion(outputs, trainY)
    loss.backward()
    optimizer.step()

    # print statistics
    print(loss.item())
    model.eval()
    val_outputs = model(valX)
    pred = softmax(val_outputs, dim=1)
    val_predictions = torch.max(pred, 1)[1]
    right = 0
    total = 0
    for i in range(val_predictions.shape[0]):
        """if val[i]['home_team'] == 'Alabama' or val[i]['away_team'] == 'Alabama' or True:
            if val_predictions[i] == 0:
                print("Predicted", val[i]['home_team'], "over", val[i]['away_team'])
            else:
                print("Predicted", val[i]['away_team'], "over", val[i]['home_team'])
            if valY[i]==0:
                print('ACTUAL: ', val[i]['home_team'])
            else:
                print('ACTUAL: ', val[i]['away_team'])"""
        if val_predictions[i] == valY[i]:
            right += 1
        total +=1
    train_preds = softmax(outputs,dim=1)
    train_preds = torch.max(train_preds,1)[1]
    train_right = 0
    train_total = 0
    for i in range(outputs.shape[0]):
        if trainY[i] == train_preds[i]:
            train_right += 1
        train_total += 1
    print("Train Accuracy:",train_right/train_total)
    print("Validation Accuracy:",right/total)



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

    valY = torch.load('tensors/validation_labels')
    trainY = torch.load('tensors/train_labels')

    ##############  HYPERPARAMETERS AND MODEL CREATION  ######################
    model = footballNN(0)
    model.to(torch.device('cuda'))
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    ##########################################################################

    print("Parameter count", sum(p.numel() for p in model.parameters() if p.requires_grad))
    for epoch in range(NUM_EPOCHS):
        print(trainX.shape)
        train_step(model, criterion, optimizer, trainX, trainY,valX,valY,val)

