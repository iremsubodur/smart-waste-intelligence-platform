import torch
import torch.nn as nn
import cv2
import numpy as np

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

model.load_state_dict(torch.load(MODEL_PATH, map_location=device))

model.to(device)
model.eval()

# =========================
# TARGET LAYER
# =========================

target_layer = model.features[-1]

gradients = None
activations = None

def backward_hook(module, grad_input, grad_output):
    global gradients
    gradients = grad_output[0]

def forward_hook(module, input, output):
    global activations
    activations = output

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
# WEBCAM
# =========================

cap = cv2.VideoCapture(0)

print("Live Grad-CAM started. Press Q to exit.")

# =========================
# LOOP
# =========================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    pil_img = Image.fromarray(rgb)

    input_tensor = transform(pil_img).unsqueeze(0).to(device)

    # forward
    output = model(input_tensor)

    probs = torch.softmax(output, dim=1)

    conf, pred = torch.max(probs, 1)

    class_idx = pred.item()

    # backward
    model.zero_grad()

    output[0, class_idx].backward()

    # =========================
    # GRAD-CAM
    # =========================

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
        (frame.shape[1], frame.shape[0])
    )

    heatmap = np.uint8(255 * heatmap)

    heatmap = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    overlay = cv2.addWeighted(
        frame,
        0.6,
        heatmap,
        0.4,
        0
    )

    # =========================
    # TEXT
    # =========================

    text = f"{CLASSES[class_idx]} ({conf.item()*100:.1f}%)"

    cv2.putText(
        overlay,
        text,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,255,255),
        2
    )

    cv2.imshow("Live Grad-CAM", overlay)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()