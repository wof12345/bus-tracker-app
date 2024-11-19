import torch

from torchvision import datasets, transforms
from torch.utils.data import DataLoader


model = torch.load(
    'classifiers/license_plate_detector.pt',
)
model.eval()


# Define transformations (e.g., resizing, normalization)
transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),  # Adjust size as needed
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

# Load your dataset
dataset = datasets.ImageFolder(root='path/to/dataset', transform=transform)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
