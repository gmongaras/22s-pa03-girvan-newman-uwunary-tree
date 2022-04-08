import yaml
import torch
import numpy as np
import os
from model import network

# Note: Change These Parameters to Configure as Discussed in the Readme

# Parameters
configFileName = "./networkParams.yml"  # The Configuration File for the Network
dataDir = "../networkTrainData"  # The Directory that Stores Data to Train Model
numEpochs = 1000  # Number of Epochs to Train the Model for
trainPercent = 1.0  # Percent Data to Train the Model on
saveFileName = "../models/model"  # File to Save the Model to

# Load Configuration File
with open(configFileName) as ymlFile:
    cfg = yaml.safe_load(ymlFile)

# Save Info from File
inDim = cfg["inDim"]
EncoderInfo = cfg["Encoder"]
DecoderInfo = cfg["Decoder"]

# Create Network
Network = network(inDim, EncoderInfo, DecoderInfo)

# Array to Hold Data
data = []

# Load in Train Data
for fileName in os.listdir(dataDir):
    with open(os.path.join(dataDir, fileName), "rb") as file:
        arr = np.load(file, allow_pickle=False)
        data.append(arr)

# Convert Data to Numpy Array
data = np.array(data)

# Create Test/Train Split of Data
trainSize = int(len(data) * trainPercent)
testSize = len(data) - trainSize
np.random.shuffle(data)
train = torch.tensor(data[0:trainSize], dtype=torch.float32, requires_grad=False)
test = torch.tensor(data[trainSize:testSize], dtype=torch.float32, requires_grad=False)

# Make Sure Train/Test Size = Model Dimensions
assert train.shape[-1] == inDim, f"The shape of the training data number be the same " \
                                 f"as the shape of the network input. Network input: {inDim}. " \
                                 f"Data shape: {train.shape[-1]}"

# Train Network for numEpochs Number of Epochs
for epoch in range(1, numEpochs + 1):

    # Get Predictions from Model
    H, M = Network(train)
    
    # Get Loss for Predictions
    loss = -Network.loss(train, M)
    
    # Get Gradients
    Network.optim.zero_grad()
    loss.backward()
    
    # Update Model
    Network.optim.step()
    print(f"Step: {epoch} \t Loss: {loss.cpu().detach().numpy().item()}")

# Save Model
Network.saveModel(saveFileName)
