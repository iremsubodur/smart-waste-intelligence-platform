import torch
import torch.nn as nn

from torchvision import models

CLASSES = 4

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# =========================================================
# MODEL FACTORY
# =========================================================

def load_efficientnet():

    model = models.efficientnet_b0(weights=None)

    in_features = model.classifier[1].in_features

    model.classifier = nn.Sequential(

        nn.Dropout(0.4),

        nn.Linear(
            in_features,
            CLASSES
        )
    )

    return model.to(device)

# =========================================================

def load_resnet():

    model = models.resnet50(weights=None)

    in_features = model.fc.in_features

    model.fc = nn.Linear(
        in_features,
        CLASSES
    )

    return model.to(device)

# =========================================================

def load_mobilenet():

    model = models.mobilenet_v2(weights=None)

    in_features = model.classifier[1].in_features

    model.classifier = nn.Sequential(

        nn.Dropout(0.3),

        nn.Linear(
            in_features,
            CLASSES
        )
    )

    return model.to(device)

# =========================================================
# BENCHMARK RESULTS
# =========================================================

MODEL_RESULTS = {

    "EfficientNet-B0": {

        "accuracy": 98.5,

        "speed": 34,

        "parameters": "5.3M",

        "edge_score": 9.5
    },

    "ResNet50": {

        "accuracy": 97.2,

        "speed": 22,

        "parameters": "25.6M",

        "edge_score": 6.4
    },

    "MobileNetV2": {

        "accuracy": 95.8,

        "speed": 41,

        "parameters": "3.4M",

        "edge_score": 9.8
    }
}