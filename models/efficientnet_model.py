import torch
import torch.nn as nn
from torchvision import models

from configs.classes import NUM_CLASSES


def build_efficientnet():
    model = models.efficientnet_b0(weights="DEFAULT")

    in_features = model.classifier[1].in_features

    model.classifier = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_features, NUM_CLASSES)
    )

    return model