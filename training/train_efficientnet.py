import os
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

import seaborn as sns
from tqdm import tqdm

from models.efficientnet_model import build_efficientnet
from utils.dataset_loader import create_dataloaders

# =========================
# DEVICE
# =========================

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"\nUsing device: {device}")

# =========================
# DATASET PATHS
# =========================

TRAIN_DIR = "datasets/waste_dataset/train"
VAL_DIR = "datasets/waste_dataset/val"

# =========================
# HYPERPARAMETERS
# =========================

BATCH_SIZE = 32
LEARNING_RATE = 0.001
EPOCHS = 10

# =========================
# LOAD DATA
# =========================

train_loader, val_loader = create_dataloaders(
    TRAIN_DIR,
    VAL_DIR,
    batch_size=BATCH_SIZE
)

# =========================
# MODEL
# =========================

model = build_efficientnet()
model = model.to(device)

# =========================
# LOSS & OPTIMIZER
# =========================

criterion = nn.CrossEntropyLoss()

optimizer = optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE
)

# =========================
# TRAINING HISTORY
# =========================

train_losses = []
val_accuracies = []

# =========================
# TRAIN LOOP
# =========================

for epoch in range(EPOCHS):

    print(f"\nEpoch {epoch+1}/{EPOCHS}")

    model.train()

    running_loss = 0.0

    for images, labels in tqdm(train_loader):

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

    epoch_loss = running_loss / len(train_loader)

    train_losses.append(epoch_loss)

    print(f"Training Loss: {epoch_loss:.4f}")

    # =========================
    # VALIDATION
    # =========================

    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)

            _, predicted = torch.max(outputs, 1)

            total += labels.size(0)

            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total

    val_accuracies.append(accuracy)

    print(f"Validation Accuracy: {accuracy:.2f}%")

# =========================
# SAVE MODEL
# =========================

os.makedirs("outputs/models", exist_ok=True)

torch.save(
    model.state_dict(),
    "outputs/models/efficientnet_waste_classifier.pth"
)

print("\nModel saved successfully.")

# =========================
# PLOT TRAINING LOSS
# =========================

plt.figure(figsize=(8, 5))

plt.plot(train_losses)

plt.title("Training Loss")

plt.xlabel("Epoch")

plt.ylabel("Loss")

plt.savefig("outputs/plots/training_loss.png")

# =========================
# PLOT VALIDATION ACCURACY
# =========================

plt.figure(figsize=(8, 5))

plt.plot(val_accuracies)

plt.title("Validation Accuracy")

plt.xlabel("Epoch")

plt.ylabel("Accuracy")

plt.savefig("outputs/plots/validation_accuracy.png")

print("\nPlots saved successfully.")
