import os
import random
import shutil

# =========================
# CONFIG
# =========================

SOURCE_DIR = "datasets/raw_dataset"
OUTPUT_DIR = "datasets/waste_dataset"

CLASSES = ["glass", "metal", "paper", "plastic"]

TRAIN_RATIO = 0.7
VAL_RATIO = 0.2
TEST_RATIO = 0.1

random.seed(42)

# =========================
# CREATE OUTPUT FOLDERS
# =========================

for split in ["train", "val", "test"]:

    for cls in CLASSES:

        path = os.path.join(OUTPUT_DIR, split, cls)

        os.makedirs(path, exist_ok=True)

# =========================
# SPLIT DATASET
# =========================

for cls in CLASSES:

    source_path = os.path.join(SOURCE_DIR, cls)

    images = os.listdir(source_path)

    random.shuffle(images)

    total = len(images)

    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)

    train_images = images[:train_end]
    val_images = images[train_end:val_end]
    test_images = images[val_end:]

    split_data = {
        "train": train_images,
        "val": val_images,
        "test": test_images
    }

    for split, image_list in split_data.items():

        for image_name in image_list:

            src = os.path.join(source_path, image_name)

            dst = os.path.join(
                OUTPUT_DIR,
                split,
                cls,
                image_name
            )

            shutil.copy(src, dst)

    print(f"{cls}")
    print(f"Train: {len(train_images)}")
    print(f"Val: {len(val_images)}")
    print(f"Test: {len(test_images)}")
    print("-" * 30)

print("\nDataset split completed.")