import os
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split

IMAGE_SIZE = 224

def get_dataloaders(raw_dir, batch_size=32):

    train_transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.RandomResizedCrop(IMAGE_SIZE),

        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(20),

        transforms.ColorJitter(
            brightness=0.25,
            contrast=0.25,
            saturation=0.25
        ),

        transforms.ToTensor(),

        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    test_transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    dataset = datasets.ImageFolder(
        root=raw_dir,
        transform=train_transform
    )

    n = len(dataset)
    train_size = int(0.7 * n)
    val_size = int(0.2 * n)
    test_size = n - train_size - val_size

    train_ds, val_ds, test_ds = random_split(
        dataset,
        [train_size, val_size, test_size]
    )

    # validation/test için farklı transform
    val_ds.dataset.transform = test_transform
    test_ds.dataset.transform = test_transform

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size)
    test_loader = DataLoader(test_ds, batch_size=batch_size)

    return train_loader, val_loader, test_loader, dataset.classes