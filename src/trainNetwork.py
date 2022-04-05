from importlib.abc import Loader
import yaml
import torch
from torch import nn
import numpy as np
import os
from model import network


# Parameters
configFileName = "./networkParams.yml"  # The configuration file for the network
dataDir = "../networkTrainData"         # The directory that stores the data to train the mode
numEpochs = 1000                        # Number of epochs to train the model for
trainPercent = 0.9                      # Percent of data to trian model on
saveFileName = "../models/model"        # The file to save the model to





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


# Make the sure train/test size is the same as the
# model dimensions
assert train.shape[-1] == inDim, f"The shape of the training data number be the same as the shape of the network input. Network input: {inDim}. Data shape: {train.shape[-1]}"


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