from torch import nn
import torch
import os


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
        
        # Get the activation functions
        if self.Encoder_activation.lower() == "sigmoid":
            enc_activation = nn.Sigmoid()
        elif self.Encoder_activation.lower() == "tanh":
            enc_activation = nn.Tanh
        elif self.Encoder_activation.lower() == "relu":
            enc_activation = nn.ReLU()
        else:
            raise RuntimeError("Activation must be ReLU, Tanh, or Sigmoid")
        
        if self.Decoder_activation.lower() == "sigmoid":
            dec_activation = nn.Sigmoid()
        elif self.Decoder_activation.lower() == "tanh":
            dec_activation = nn.Tanh
        elif self.Decoder_activation.lower() == "relu":
            dec_activation = nn.ReLU()
        else:
            raise RuntimeError("Activation must be ReLU, Tanh, or Sigmoid")
        
        # Create the Encoder
        layers = []
        for l in range(0, len(self.Encoder_layers)-2):
            layers.append(nn.Linear(self.Encoder_layers[l], self.Encoder_layers[l+1]))
            layers.append(enc_activation)
        layers.append(nn.Linear(self.Encoder_layers[l+1], self.Encoder_layers[l+2]))
        self.Encoder = nn.Sequential(*layers)
        
        # Create the Decoder
        layers = []
        for l in range(0, len(self.Decoder_layers)-2):
            layers.append(nn.Linear(self.Decoder_layers[l], self.Decoder_layers[l+1]))
            layers.append(dec_activation)
        layers.append(nn.Linear(self.Decoder_layers[l+1], self.Decoder_layers[l+2]))
        self.Decoder = nn.Sequential(*layers)
        
        # Optimizer for the model
        self.optim = torch.optim.Adam(self.parameters())
    
    
    
    # Get a prediction from the network
    # Input:
    #   X - The input into the model
    # Output:
    #   H - The encoded form of the input in the latent space
    #   M - The rebuilt form of H which should match X
    def forward(self, X):
        H = self.Encoder(X)
        M = self.Decoder(H)
        return H, M

    
    
    # The Cross-Entropy loss for the model
    # Inputs:
    #   m_i - The labels, what we want to get
    #   b_i - The predictions from the model
    def loss(self, m_i, b_i):
        # Get the sigmoid values
        sigmoid_m = torch.sigmoid(m_i)
        sigmoid_b = torch.sigmoid(b_i)
        
        # Ensure the values don't produce a NaN value
        sigmoid_b = torch.where(sigmoid_b == 0, sigmoid_b+0.0000001, sigmoid_b)
        sigmoid_b = torch.where(sigmoid_b == 1, sigmoid_b-0.0000001, sigmoid_b)
        
        # Get the two terms in the loss function
        T1 = sigmoid_m*torch.log(sigmoid_b)
        T2 = (1-sigmoid_m)*torch.log(1-sigmoid_b)
        
        # Sum up the terms and return the values
        loss = torch.sum(T1 + T2)
        return loss

    
    
    # Save the model to the specified file
    def saveModel(self, fileName):
        # Get the last separator in the filename
        dirName = "/".join(fileName.split("/")[0:-1])
    
        # If the directory doesn't exist, create it
        try:
            if (not os.path.isdir(dirName) and dirName != ''):
                os.makedirs(dirName, exist_ok=True)
        
            torch.save(self.state_dict(), fileName)
        
        except:
            torch.save(self.state_dict(), fileName)
    
    
    # Load a model from a file
    def loadModel(self, fileName):
        # If the file doesn't exist, raise an error
        if (not os.path.isfile(fileName)):
            raise Exception("Specified model file does no exist")
        
        # Load the model
        self.load_state_dict(torch.load(fileName))
        self.eval()