# -*- coding: utf-8 -*-
"""Untitled44.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/113GAwF6tC6YkTZ0H-DowJyVZC2sNN2-s
"""

import torchvision.models as models
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from sklearn.model_selection import train_test_split

# Define your dataset class
class CustomDataset(Dataset):
    def __init__(self, data, labels, transform=None):
        self.data = data
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_path = self.data[idx]
        image = Image.open(img_path).convert("RGB")

        if self.transform:
            image = self.transform(image)

        label = self.labels[idx]
        return image, label

image_folder = "/content/"

# Update the paths accordingly
train_data_paths = [image_folder + "imageset_train/" + img + ".jpg" for img in imageset_train]
test_data_paths = [image_folder + "imageset_test/" + img + ".jpg" for img in imageset_test]

# Split the training set into training and validation sets
train_data_paths, val_data_paths, train_labels, val_labels = train_test_split(
    train_data_paths, train_labels, test_size=0.2, random_state=42
)

# Define data transformations
transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
])

# Create dataset instances
train_dataset = CustomDataset(train_data_paths, train_labels, transform=transform)
val_dataset = CustomDataset(val_data_paths, val_labels, transform=transform)
test_dataset = CustomDataset(test_data_paths, test_labels, transform=transform)

# Create data loaders
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# Define the CNN architecture
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=15):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(16 * 32 * 32, num_classes)

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)
        x = x.view(-1, 16 * 32 * 32)
        x = self.fc1(x)
        return x

# Instantiate the model
model = SimpleCNN()

# Define a loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 10

for epoch in range(num_epochs):
    model.train()
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

# Evaluation on the validation set
model.eval()
correct = 0
total = 0

with torch.no_grad():
    for inputs, labels in val_loader:
        outputs = model(inputs)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = correct / total
print(f'Validation Accuracy: {accuracy * 100:.2f}%')

# Evaluation on the test set
model.eval()
correct = 0
total = 0

with torch.no_grad():
    for inputs, labels in test_loader:
        outputs = model(inputs)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = correct / total
print(f'Test Accuracy: {accuracy * 100:.2f}%')


# LeNet-5 Model
class LeNet5(nn.Module):
    def __init__(self, num_classes=15):
        super(LeNet5, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, kernel_size=5, stride=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5, stride=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(16 * 13 * 13, 120)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(120, 84)
        self.relu4 = nn.ReLU()
        self.fc3 = nn.Linear(84, num_classes)

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.pool2(x)
        x = x.view(-1, 16 * 13 * 13)
        x = self.fc1(x)
        x = self.relu3(x)
        x = self.fc2(x)
        x = self.relu4(x)
        x = self.fc3(x)
        return x

# Instantiate the LeNet-5 model
lenet_model = LeNet5()

# Define a loss function and optimizer for LeNet-5
criterion_lenet = nn.CrossEntropyLoss()
optimizer_lenet = optim.Adam(lenet_model.parameters(), lr=0.001)

# Training loop for LeNet-5
num_epochs_lenet = 10

for epoch in range(num_epochs_lenet):
    lenet_model.train()
    for inputs, labels in train_loader:
        optimizer_lenet.zero_grad()
        outputs = lenet_model(inputs)
        loss = criterion_lenet(outputs, labels)
        loss.backward()
        optimizer_lenet.step()

# Evaluation on the validation set for LeNet-5
lenet_model.eval()
correct = 0
total = 0

with torch.no_grad():
    for inputs, labels in val_loader:
        outputs = lenet_model(inputs)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = correct / total
print(f'LeNet-5 Validation Accuracy: {accuracy * 100:.2f}%')

# Evaluation on the test set for LeNet-5
lenet_model.eval()
correct = 0
total = 0

with torch.no_grad():
    for inputs, labels in test_loader:
        outputs = lenet_model(inputs)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = correct / total
print(f'LeNet-5 Test Accuracy: {accuracy * 100:.2f}%')

# VGG-16 Model
class VGG16(nn.Module):
    def __init__(self, num_classes=15):
        super(VGG16, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Linear(256 * 8 * 8, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

# Instantiate the VGG-16 model
vgg16_model = VGG16()

# Define a loss function and optimizer for VGG-16
criterion_vgg16 = nn.CrossEntropyLoss()
optimizer_vgg16 = optim.Adam(vgg16_model.parameters(), lr=0.001)

# Training loop for VGG-16
num_epochs_vgg16 = 10

for epoch in range(num_epochs_vgg16):
    vgg16_model.train()
    for inputs, labels in train_loader:
        optimizer_vgg16.zero_grad()
        outputs = vgg16_model(inputs)
        loss = criterion_vgg16(outputs, labels)
        loss.backward()
        optimizer_vgg16.step()

# Evaluation on the validation set for VGG-16
vgg16_model.eval()
correct = 0
total = 0

with torch.no_grad():
    for inputs, labels in val_loader:
        outputs = vgg16_model(inputs)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = correct / total
print(f'VGG-16 Validation Accuracy: {accuracy * 100:.2f}%')

# Evaluation on the test set for VGG-16
vgg16_model.eval()
correct = 0
total = 0

with torch.no_grad():
    for inputs, labels in test_loader:
        outputs = vgg16_model(inputs)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = correct / total
print(f'VGG-16 Test Accuracy: {accuracy * 100:.2f}%')