import torch
import torch.nn as nn
import cv2
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from torchvision import transforms, models

from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image

# =========================
# CONFIG
# =========================

CLASSES = ["glass", "metal", "paper", "plastic"]

IMAGE_PATH = "test.jpg"

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
# TARGET LAYER
# =========================

target_layers = [model.features[-1]]

# =========================
# IMAGE
# =========================

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

image = Image.open(IMAGE_PATH).convert("RGB")

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
# GRADCAM
# =========================

cam = GradCAM(
    model=model,
    target_layers=target_layers
)

grayscale_cam = cam(
    input_tensor=input_tensor
)[0]

# =========================
# VISUALIZATION
# =========================

rgb_image = np.array(image.resize((224, 224))) / 255.0

visualization = show_cam_on_image(
    rgb_image,
    grayscale_cam,
    use_rgb=True
)

# =========================
# PLOT
# =========================

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(rgb_image)
plt.title("Original")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(visualization)
plt.title(
    f"{predicted_class} ({confidence.item()*100:.2f}%)"
)
plt.axis("off")

plt.tight_layout()

plt.show()