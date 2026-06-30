import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import matplotlib.pyplot as plt

CLASSES = ["glass", "metal", "paper", "plastic"]

device = torch.device("cpu")

# =========================
# LOAD MODEL
# =========================

model = models.efficientnet_b0(weights=None)

in_features = model.classifier[1].in_features

model.classifier = nn.Sequential(
    nn.Dropout(0.3),
    nn.Linear(in_features, len(CLASSES))
)

model.load_state_dict(
    torch.load(
        "outputs/models/model.pth",
        map_location=device
    )
)

model.eval()

# =========================
# IMAGE TRANSFORM
# =========================

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# =========================
# LOAD IMAGE
# =========================

image_path = "test.jpg"

image = Image.open(image_path).convert("RGB")

input_tensor = transform(image).unsqueeze(0)

# =========================
# PREDICTION
# =========================

with torch.no_grad():

    output = model(input_tensor)

    probabilities = torch.softmax(output[0], dim=0)

    confidence, predicted = torch.max(probabilities, 0)

predicted_class = CLASSES[predicted.item()]

print("\nPrediction:", predicted_class)
print("Confidence:", round(confidence.item() * 100, 2), "%")

# =========================
# SHOW IMAGE
# =========================

plt.imshow(image)

plt.title(
    f"{predicted_class} ({confidence.item()*100:.2f}%)"
)

plt.axis("off")

plt.show()