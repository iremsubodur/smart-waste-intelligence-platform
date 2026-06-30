import os
import shutil

BASE_DIR = "datasets/raw_dataset"

CLASSES = ["glass", "metal", "paper", "plastic"]

VALID_EXTENSIONS = (".jpg", ".jpeg", ".png")

for cls in CLASSES:

    class_path = os.path.join(BASE_DIR, cls)

    for root, dirs, files in os.walk(class_path):

        # ana klasörü geç
        if root == class_path:
            continue

        for file in files:

            if file.lower().endswith(VALID_EXTENSIONS):

                src = os.path.join(root, file)

                dst = os.path.join(class_path, file)

                # aynı isim varsa çakışmayı önle
                if os.path.exists(dst):

                    name, ext = os.path.splitext(file)

                    counter = 1

                    while os.path.exists(dst):

                        new_name = f"{name}_{counter}{ext}"

                        dst = os.path.join(class_path, new_name)

                        counter += 1

                shutil.move(src, dst)

                print(f"Moved: {src}")

print("\nDataset flattening completed.")