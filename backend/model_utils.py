import torch
import torch.nn as nn
import cv2
import numpy as np
from PIL import Image
from torchvision import transforms

# Model Architecture (same as notebook)
class UltimateCNN(nn.Module):
    def __init__(self, num_classes=4):
        super().__init__()
        self.conv1 = nn.Sequential(nn.Conv2d(3, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(), nn.MaxPool2d(2))
        self.conv2 = nn.Sequential(nn.Conv2d(64, 128, 3, padding=1), nn.BatchNorm2d(128), nn.ReLU(), nn.MaxPool2d(2))
        self.conv3a = nn.Sequential(nn.Conv2d(128, 256, 3, padding=1), nn.BatchNorm2d(256), nn.ReLU())
        self.conv3b = nn.Sequential(nn.Conv2d(256, 256, 3, padding=1), nn.BatchNorm2d(256), nn.ReLU(), nn.MaxPool2d(2))
        self.conv4a = nn.Sequential(nn.Conv2d(256, 512, 3, padding=1), nn.BatchNorm2d(512), nn.ReLU())
        self.conv4b = nn.Sequential(nn.Conv2d(512, 512, 3, padding=1), nn.BatchNorm2d(512), nn.ReLU(), nn.MaxPool2d(2))
        self.conv5a = nn.Sequential(nn.Conv2d(512, 1024, 3, padding=1), nn.BatchNorm2d(1024), nn.ReLU())
        self.conv5b = nn.Sequential(nn.Conv2d(1024, 1024, 3, padding=1), nn.BatchNorm2d(1024), nn.ReLU(), nn.MaxPool2d(2))
        
        self.global_pool = nn.AdaptiveAvgPool2d(1)
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(1024, 512), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(512, 256), nn.ReLU(), nn.Dropout(0.4),
            nn.Linear(256, 128), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )
    
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3a(x); x = self.conv3b(x)
        x = self.conv4a(x); x = self.conv4b(x)
        x = self.conv5a(x); x = self.conv5b(x)
        x = self.global_pool(x); x = self.classifier(x)
        return x


def preprocess_image(image_bytes):
    """Preprocess image using the same pipeline as training"""
    # Validate input
    if not image_bytes or len(image_bytes) == 0:
        raise ValueError("Image bytes are empty")
    
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    
    if len(nparr) == 0:
        raise ValueError("Image buffer is empty after conversion")
    
    # Try to decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        # Try alternative: read as color and convert to grayscale
        img_color = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img_color is None:
            raise ValueError(f"Could not decode image. Image size: {len(image_bytes)} bytes")
        img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    
    if img is None or img.size == 0:
        raise ValueError("Decoded image is empty or invalid")
    
    # CLAHE enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img = clahe.apply(img)
    
    # Threshold and contour detection for cropping
    _, thresh = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        cnt = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)
        margin = 20
        img = img[max(0, y-margin):min(img.shape[0], y+h+margin), 
                 max(0, x-margin):min(img.shape[1], x+w+margin)]
    
    # Resize to 224x224
    img = cv2.resize(img, (224, 224))
    
    # Convert to RGB (3 channels)
    img_rgb = np.stack([img, img, img], axis=2)
    image = Image.fromarray(img_rgb)
    
    # Apply transforms
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.5]*3, [0.5]*3)
    ])
    
    tensor = transform(image).unsqueeze(0)  # Add batch dimension
    return tensor


def load_model(model_path, device='cpu'):
    """Load the trained model"""
    import os
    
    # Validate file exists and is not empty
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    file_size = os.path.getsize(model_path)
    if file_size == 0:
        raise ValueError(f"Model file is empty: {model_path}")
    
    # Check if file looks like a PyTorch model (should start with specific bytes)
    with open(model_path, 'rb') as f:
        first_bytes = f.read(4)
        # PyTorch files typically start with specific magic numbers
        # If it starts with text characters, it's likely corrupted
        if first_bytes.startswith(b'PK') or first_bytes.startswith(b'\x80'):
            # Looks like a valid binary file
            pass
        elif first_bytes.decode('utf-8', errors='ignore').isprintable():
            raise ValueError(
                f"Model file appears to be text/corrupted, not a binary PyTorch file: {model_path}\n"
                f"File size: {file_size} bytes. Expected a binary .pth file saved with torch.save()."
            )
    
    try:
        model = UltimateCNN(num_classes=4)
        state_dict = torch.load(model_path, map_location=device, weights_only=False)
        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()
        print(f"✅ Model loaded: {file_size:,} bytes, {sum(p.numel() for p in model.parameters()):,} parameters")
        return model
    except Exception as e:
        raise RuntimeError(
            f"Failed to load model from {model_path}.\n"
            f"Error: {str(e)}\n"
            f"File size: {file_size} bytes.\n"
            f"Please ensure the file is a valid PyTorch model saved with torch.save(model.state_dict(), 'best_cnn.pth')"
        ) from e


def predict(model, image_tensor, device='cpu'):
    """Make prediction on preprocessed image"""
    classes = ['glioma', 'meningioma', 'pituitary', 'notumor']
    
    with torch.no_grad():
        image_tensor = image_tensor.to(device)
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
        
        pred_class = classes[predicted.item()]
        confidence_score = confidence.item()
        
        # Get all class probabilities
        all_probs = probabilities[0].cpu().numpy()
        class_probs = {classes[i]: float(all_probs[i]) for i in range(len(classes))}
        
        return pred_class, confidence_score, class_probs

