import cv2
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
import time

# =========================================================
# CONFIG
# =========================================================

CLASSES = [
    "glass",
    "metal",
    "paper",
    "plastic"
]

MODEL_PATH = "best_model.pth"

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"Using device: {device}")

# =========================================================
# LOAD MODEL
# =========================================================

model = models.efficientnet_b0(weights=None)

in_features = model.classifier[1].in_features

model.classifier = nn.Sequential(

    nn.Dropout(0.4),

    nn.Linear(
        in_features,
        len(CLASSES)
    )
)

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=device
    )
)

model.to(device)

model.eval()

# =========================================================
# IMAGE TRANSFORM
# =========================================================

transform = transforms.Compose([

    transforms.Resize((224, 224)),

    transforms.ToTensor(),

    transforms.Normalize(

        mean=[0.485, 0.456, 0.406],

        std=[0.229, 0.224, 0.225]
    )
])

# =========================================================
# WEBCAM
# =========================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("Webcam could not be opened.")
    exit()

# =========================================================
# FPS VARIABLES
# =========================================================

prev_frame_time = 0
new_frame_time = 0

# =========================================================
# MAIN LOOP
# =========================================================

while True:

    success, frame = cap.read()

    if not success:

        break

    # =====================================================
    # FPS CALCULATION
    # =====================================================

    new_frame_time = time.time()

    fps = 1 / (new_frame_time - prev_frame_time)

    prev_frame_time = new_frame_time

    fps = int(fps)

    # =====================================================
    # IMAGE PREPROCESS
    # =====================================================

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    pil_image = Image.fromarray(rgb)

    tensor = transform(pil_image) \
        .unsqueeze(0) \
        .to(device)

    # =====================================================
    # PREDICTION
    # =====================================================

    with torch.no_grad():

        output = model(tensor)

        probs = torch.softmax(
            output,
            dim=1
        )[0]

    predicted_index = torch.argmax(probs).item()

    predicted_class = CLASSES[predicted_index]

    confidence = probs[predicted_index].item() * 100

    # =====================================================
    # UI OVERLAY
    # =====================================================

    cv2.putText(

        frame,

        f"{predicted_class} ({confidence:.2f}%)",

        (20, 40),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.9,

        (0, 255, 0),

        2
    )

    cv2.putText(

        frame,

        f"FPS: {fps}",

        (20, 80),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.8,

        (0, 255, 255),

        2
    )

    cv2.putText(

        frame,

        f"Device: {device}",

        (20, 120),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.7,

        (255, 255, 0),

        2
    )

    # =====================================================
    # SHOW FRAME
    # =====================================================

    cv2.imshow(
        "AI Smart Waste Detection",
        frame
    )

    # =====================================================
    # EXIT
    # =====================================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break

# =========================================================
# CLEANUP
# =========================================================

cap.release()

cv2.destroyAllWindows()