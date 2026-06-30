import torch
import torch.nn as nn
import numpy as np
import cv2

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
# TARGET LAYER
# =========================

target_layer = model.features[-1]

gradients = None
activations = None

def forward_hook(module, input, output):
    global activations
    activations = output

def backward_hook(module, grad_input, grad_output):
    global gradients
    gradients = grad_output[0]

target_layer.register_forward_hook(forward_hook)
target_layer.register_full_backward_hook(backward_hook)

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
# GENERATE GRADCAM
# =========================

def generate_gradcam(image):

    img = image.convert("RGB")

    original = np.array(img)

    pil_img = Image.fromarray(original)

    tensor = transform(pil_img).unsqueeze(0).to(device)

    output = model(tensor)

    pred_class = output.argmax(dim=1).item()

    model.zero_grad()

    output[0, pred_class].backward()

    pooled_gradients = torch.mean(
        gradients,
        dim=[0, 2, 3]
    )

    activation = activations[0]

    for i in range(len(pooled_gradients)):
        activation[i, :, :] *= pooled_gradients[i]

    heatmap = torch.mean(activation, dim=0).cpu().detach().numpy()

    heatmap = np.maximum(heatmap, 0)

    heatmap /= np.max(heatmap)

    heatmap = cv2.resize(
        heatmap,
        (original.shape[1], original.shape[0])
    )

    heatmap = np.uint8(255 * heatmap)

    heatmap = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    overlay = cv2.addWeighted(
        original,
        0.6,
        heatmap,
        0.4,
        0
    )

    return overlay