import torch
from torchvision import models

print("Torch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

# test model load
model = models.efficientnet_b0(weights=None)

print("Model loaded successfully")