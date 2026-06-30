import torch
import torch.nn as nn

from torchvision import models, transforms
from PIL import Image

# =========================
# CONFIG
# =========================

CLASSES = ["glass", "metal", "paper", "plastic"]

MODEL_PATH = "best_model.pth"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =========================
# MODEL
# =========================

model = models.efficientnet_b0(weights=None)

in_features = model.classifier[1].in_features

model.classifier = nn.Sequential(
    nn.Dropout(0.4),
    nn.Linear(in_features, len(CLASSES))
)

model.load_state_dict(
    torch.load(MODEL_PATH, map_location=device)
)

model.to(device)
model.eval()

# =========================
# TRANSFORM
# =========================

transform = transforms.Compose([

    transforms.Resize((224, 224)),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# =========================
# PREDICT FUNCTION
# =========================

def predict_image(image):

    img = image.convert("RGB")

    tensor = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():

        output = model(tensor)

        probs = torch.softmax(output, dim=1)[0]

    predictions = {}

    for i, c in enumerate(CLASSES):

        predictions[c] = float(probs[i])

    best_class = max(predictions, key=predictions.get)

    return best_class, predictions