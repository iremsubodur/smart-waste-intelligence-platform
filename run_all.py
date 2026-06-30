import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from torch.optim import Adam
import pandas as pd
import numpy as np

# =========================================================
# DEVICE
# =========================================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"Device: {device}")

# =========================================================
# CONFIG
# =========================================================

DATASET_DIR = "datasets/raw_dataset"

CLASSES = [
    "glass",
    "metal",
    "paper",
    "plastic"
]

IMAGE_SIZE = 224

BATCH_SIZE = 16

EPOCHS = 5

LEARNING_RATE = 0.0001

# =========================================================
# LOAD DATA PATHS
# =========================================================

image_paths = []

labels = []

for class_index, class_name in enumerate(CLASSES):

    class_folder = os.path.join(
        DATASET_DIR,
        class_name
    )

    if not os.path.exists(class_folder):

        print(f"SKIP {class_name} (folder missing)")

        continue

    files = os.listdir(class_folder)

    print(f"{class_name}: {len(files)} images")

    for file in files:

        full_path = os.path.join(
            class_folder,
            file
        )

        image_paths.append(full_path)

        labels.append(class_index)

print(f"\nTotal Images: {len(image_paths)}")

# =========================================================
# CHECK DATA
# =========================================================

if len(image_paths) == 0:

    raise Exception(
        "Dataset is empty. Check dataset folder structure."
    )

# =========================================================
# TRAIN / VALIDATION SPLIT
# =========================================================

train_paths, val_paths, train_labels, val_labels = train_test_split(

    image_paths,
    labels,

    test_size=0.2,

    random_state=42,

    stratify=labels
)

print(f"Train Images: {len(train_paths)}")

print(f"Validation Images: {len(val_paths)}")

# =========================================================
# TRANSFORMS
# =========================================================

train_transform = transforms.Compose([

    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),

    transforms.RandomHorizontalFlip(),

    transforms.RandomRotation(10),

    transforms.ColorJitter(

        brightness=0.2,
        contrast=0.2,
        saturation=0.2
    ),

    transforms.ToTensor(),

    transforms.Normalize(

        mean=[0.485, 0.456, 0.406],

        std=[0.229, 0.224, 0.225]
    )
])

val_transform = transforms.Compose([

    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),

    transforms.ToTensor(),

    transforms.Normalize(

        mean=[0.485, 0.456, 0.406],

        std=[0.229, 0.224, 0.225]
    )
])

# =========================================================
# CUSTOM DATASET
# =========================================================

class WasteDataset(Dataset):

    def __init__(

        self,
        image_paths,
        labels,
        transform=None
    ):

        self.image_paths = image_paths

        self.labels = labels

        self.transform = transform

    def __len__(self):

        return len(self.image_paths)

    def __getitem__(self, idx):

        image = Image.open(
            self.image_paths[idx]
        ).convert("RGB")

        label = self.labels[idx]

        if self.transform:

            image = self.transform(image)

        return image, label

# =========================================================
# DATASETS
# =========================================================

train_dataset = WasteDataset(

    train_paths,
    train_labels,
    transform=train_transform
)

val_dataset = WasteDataset(

    val_paths,
    val_labels,
    transform=val_transform
)

# =========================================================
# DATALOADERS
# =========================================================

train_loader = DataLoader(

    train_dataset,

    batch_size=BATCH_SIZE,

    shuffle=True
)

val_loader = DataLoader(

    val_dataset,

    batch_size=BATCH_SIZE,

    shuffle=False
)

# =========================================================
# MODEL
# =========================================================

model = models.efficientnet_b0(weights="DEFAULT")

in_features = model.classifier[1].in_features

model.classifier = nn.Sequential(

    nn.Dropout(0.4),

    nn.Linear(
        in_features,
        len(CLASSES)
    )
)

model.to(device)

# =========================================================
# LOSS + OPTIMIZER
# =========================================================

criterion = nn.CrossEntropyLoss()

optimizer = Adam(

    model.parameters(),

    lr=LEARNING_RATE
)

# =========================================================
# TRAINING HISTORY
# =========================================================

train_losses = []

val_accuracies = []

best_accuracy = 0

# =========================================================
# TRAINING LOOP
# =========================================================

for epoch in range(EPOCHS):

    model.train()

    running_loss = 0

    for images, labels in train_loader:

        images = images.to(device)

        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

    avg_loss = running_loss / len(train_loader)

    train_losses.append(avg_loss)

    # =====================================================
    # VALIDATION
    # =====================================================

    model.eval()

    correct = 0

    total = 0

    all_predictions = []

    all_labels = []

    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(device)

            labels = labels.to(device)

            outputs = model(images)

            _, predicted = torch.max(outputs, 1)

            total += labels.size(0)

            correct += (predicted == labels).sum().item()

            all_predictions.extend(
                predicted.cpu().numpy()
            )

            all_labels.extend(
                labels.cpu().numpy()
            )

    accuracy = 100 * correct / total

    val_accuracies.append(accuracy)

    print(f"\nEpoch {epoch+1}/{EPOCHS}")

    print(f"Loss: {avg_loss:.4f}")

    print(f"Validation Accuracy: {accuracy:.2f}%")

    # =====================================================
    # SAVE BEST MODEL
    # =====================================================

    if accuracy > best_accuracy:

        best_accuracy = accuracy

        torch.save(

            model.state_dict(),

            "best_model.pth"
        )

        print("Best model updated.")

# =========================================================
# CONFUSION MATRIX
# =========================================================

cm = confusion_matrix(

    all_labels,
    all_predictions
)

cm_df = pd.DataFrame(

    cm,

    index=CLASSES,

    columns=CLASSES
)

cm_df.to_csv(

    "confusion_matrix.csv"
)

print("\nConfusion matrix saved.")

# =========================================================
# CLASSIFICATION REPORT
# =========================================================

report = classification_report(

    all_labels,
    all_predictions,

    target_names=CLASSES
)

with open(

    "classification_report.txt",

    "w"
) as f:

    f.write(report)

print("Classification report saved.")

# =========================================================
# TRAINING HISTORY
# =========================================================

history_df = pd.DataFrame({

    "epoch": list(range(1, EPOCHS + 1)),

    "loss": train_losses,

    "validation_accuracy": val_accuracies
})

history_df.to_csv(

    "training_history.csv",

    index=False
)

print("Training history saved.")

# =========================================================
# FINAL RESULTS
# =========================================================

print("\nTraining Complete")

print(f"Best Validation Accuracy: {best_accuracy:.2f}%")

print("\nSaved Files:")

print("- best_model.pth")

print("- training_history.csv")

print("- confusion_matrix.csv")

print("- classification_report.txt")