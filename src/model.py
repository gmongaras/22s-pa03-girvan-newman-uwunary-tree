from torch import nn
import torch
import os

device = torch.device('cpu')
if torch.cuda.is_available():
    device = torch.device('cuda')


# Initialize Network
class network(nn.Module):

    # Inputs:
    # inDim = Size of the Dimension to Encode
    # EncoderInfo = Info on Encoder Network
    # DecoderInfo - Info on th decoder network
    def __init__(self, inDim, EncoderInfo, DecoderInfo):
        super(network, self).__init__()
        
        # Save Information
        self.inDim = inDim
        self.Encoder_layers = [inDim] + EncoderInfo["layerNodes"]
        self.Encoder_activation = EncoderInfo["activation"]
        self.Decoder_layers = DecoderInfo["layerNodes"] + [inDim]
        self.Decoder_activation = DecoderInfo["activation"]
        
        # Get Activation Functions
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
        
        # Create Encoder
        layers = []
        for l in range(0, len(self.Encoder_layers)-2):
            layers.append(nn.Linear(self.Encoder_layers[l], self.Encoder_layers[l+1]))
            layers.append(enc_activation)
        layers.append(nn.Linear(self.Encoder_layers[l+1], self.Encoder_layers[l+2]))
        self.Encoder = nn.Sequential(*layers).to(device)
        
        # Create Decoder
        layers = []
        for l in range(0, len(self.Decoder_layers)-2):
            layers.append(nn.Linear(self.Decoder_layers[l], self.Decoder_layers[l+1]))
            layers.append(dec_activation)
        layers.append(nn.Linear(self.Decoder_layers[l+1], self.Decoder_layers[l+2]))
        self.Decoder = nn.Sequential(*layers).to(device)
        
        # Optimizer for Model
        self.optim = torch.optim.Adam(self.parameters())

    # Get Prediction from Network
    # Input:
    # X = The Input into Model
    # Output:
    # H - The Encoded Form of the Input in the Latent Space
    # M - The Rebuilt Form of H Which Should Match X
    def forward(self, X):
        X = X.to(device)
        H = self.Encoder(X)
        M = self.Decoder(H)
        return H, M

    # The Cross-Entropy Loss for the Model
    # Inputs:
    # m_i = The Labels, What we Want
    # b_i - The Predictions from the Model
    def loss(self, m_i, b_i):

        # Get Sigmoid Values
        sigmoid_m = torch.sigmoid(m_i).to(device)
        sigmoid_b = torch.sigmoid(b_i).to(device)
        
        # Ensure Values don't Produce a NaN
        sigmoid_b = torch.where(sigmoid_b == 0, sigmoid_b+0.0000001, sigmoid_b)
        sigmoid_b = torch.where(sigmoid_b == 1, sigmoid_b-0.0000001, sigmoid_b)
        
        # Get Two Terms in Loss Function
        T1 = sigmoid_m*torch.log(sigmoid_b)
        T2 = (1-sigmoid_m)*torch.log(1-sigmoid_b)
        
        # Sum up Terms and Return Values
        loss = torch.sum(T1 + T2)
        return loss

    # Save Model to Specified File
    def saveModel(self, fileName):

        # Get Last Separator in the Filename
        dirName = "/".join(fileName.split("/")[0:-1])
    
        # If the Directory doesn't Exist, Create it
        try:
            if not os.path.isdir(dirName) and dirName != '':
                os.makedirs(dirName, exist_ok=True)
            torch.save(self.state_dict(), fileName)
        except:
            torch.save(self.state_dict(), fileName)

    # Load Model from File
    def loadModel(self, fileName):

        # If the File doesn't Exist, Raise an Error
        if not os.path.isfile(fileName):
            raise Exception("Specified model file does no exist")
        
        # Load Model
        try:
            self.load_state_dict(torch.load(fileName, map_location=device))
        except:
            raise RuntimeError("The network has different parameters than the model that's being loaded in.")
        self.eval()
