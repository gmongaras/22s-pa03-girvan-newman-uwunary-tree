from importlib.abc import Loader
import yaml
import torch
from torch import nn
import numpy as np
import os
from model import network


# Parameters
configFileName = "./networkParams.yml"
dataDir = "../networkTrainData"
numEpochs = 1000
trainPercent = 0.9
saveFileName = "../models/model"





# Load the configuration file
with open(configFileName) as ymlFile:
    cfg = yaml.safe_load(ymlFile)

# Save the info from the file
inDim = cfg["inDim"]
EncoderInfo = cfg["Encoder"]
DecoderInfo = cfg["Decoder"]


# Create the network
Network = network(inDim, EncoderInfo, DecoderInfo)


# The array to hold the data
data = []

# Load in the train data
for fileName in os.listdir(dataDir):
    with open(os.path.join(dataDir, fileName), "rb") as file:
        arr = np.load(file, allow_pickle=False)
        data.append(arr)

# Convert the data to a numpy array
data = np.array(data)


# Create a test/train split of the data
trainSize = int(len(data)*trainPercent)
testSize = len(data) - trainSize
np.random.shuffle(data)
train = torch.tensor(data[0:trainSize], dtype=torch.float32, requires_grad=False)
test = torch.tensor(data[trainSize:testSize], dtype=torch.float32, requires_grad=False)


# Train the network for numEpochs number of epochs
for epoch in range(1, numEpochs+1):
    # Get predictions from the model
    H, M = Network(train)
    
    # Get the loss for the predictions
    loss = -Network.loss(train, M)
    
    # Get the gradients
    Network.optim.zero_grad()
    loss.backward()
    
    # Update the model
    Network.optim.step()
    print(f"Step: {epoch} \t Loss: {loss.cpu().detach().numpy().item()}")

# Save the model
Network.saveModel(saveFileName)