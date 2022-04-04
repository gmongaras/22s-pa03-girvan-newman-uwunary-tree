from importlib.abc import Loader
import yaml
from torch import nn
import numpy as np
import os


# Parameters
configFileName = "./networkParams.yml"
dataDir = "../networkTrainData"
numEpochs = 1000




class network(nn.Module):
    # Initialize the network
    # Inputs:
    #   inDim - The size of the dimension to encode
    #   EncoderInfo - Info on the encoder network
    #   DecoderInfo - Info on th decoder network
    def __init__(self, inDim, EncoderInfo, DecoderInfo):
        super(network, self).__init__()
        
        # Save the information
        self.inDim = inDim
        self.Encoder_layers = [inDim] + EncoderInfo["layerNodes"]
        self.Encoder_activation = EncoderInfo["activation"]
        self.Decoder_layers = DecoderInfo["layerNodes"] + [inDim]
        self.Decoder_activation = DecoderInfo["activation"]
        
        # Create the Encoder
        layers = []
        for l in range(0, len(self.Encoder_layers)-1):
            layers.append(nn.Linear(self.Encoder_layers[l], self.Encoder_layers[l+1]))
        self.Encoder = nn.Sequential(*layers)
        
        # Create the Decoder
        layers = []
        for l in range(0, len(self.Decoder_layers)-1):
            layers.append(nn.Linear(self.Decoder_layers[l], self.Decoder_layers[l+1]))
        self.Decoder = nn.Sequential(*layers)
    
    
    
    # Get a prediction from the network
    def forward():
        print()





# Load the configuration file
with open(configFileName) as ymlFile:
    cfg = yaml.safe_load(ymlFile)

# Save the info from the file
inDim = cfg["inDim"]
EncoderInfo = cfg["Encoder"]
DecoderInfo = cfg["Decoder"]


# Create the networks
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



# Train the network for numEpochs number of epochs
for epoch in range(1, numEpochs+1):
    print()