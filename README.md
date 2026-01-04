# Brain Tumor Detection using CNN

## Project Overview

This project implements a deep learning-based approach for brain tumor classification using Convolutional Neural Networks (CNNs). The application is built using FastAPI (backend) and Streamlit (frontend) to provide a web interface for users to upload MRI images and obtain predictions. The model classifies MRI scans into four categories:

- **Glioma**
- **Meningioma**
- **No Tumor**
- **Pituitary Tumor**

The project includes a complete full-stack implementation with REST API backend and modern web frontend.

## Dataset

The dataset used for training and evaluation can be accessed from Kaggle: 🔗 [Brain Tumor MRI Dataset](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset)

The dataset consists of MRI scan images labeled according to the tumor type. Preprocessing steps include:
- CLAHE (Contrast Limited Adaptive Histogram Equalization) enhancement
- Thresholding and contour detection for brain region extraction
- Resizing images to 224x224
- Normalization and data augmentation

## Network Architecture

The CNN model (UltimateCNN) comprises multiple convolutional layers with batch normalization, ReLU activation, and max-pooling. The extracted features are then passed through fully connected layers for classification.

### Model Structure:

**Convolutional Layers:**
- Conv2D(3→64, kernel_size=3) → BatchNorm → ReLU() → MaxPool2D(2,2)
- Conv2D(64→128, kernel_size=3) → BatchNorm → ReLU() → MaxPool2D(2,2)
- Conv2D(128→256, kernel_size=3) → BatchNorm → ReLU()
- Conv2D(256→256, kernel_size=3) → BatchNorm → ReLU() → MaxPool2D(2,2)
- Conv2D(256→512, kernel_size=3) → BatchNorm → ReLU()
- Conv2D(512→512, kernel_size=3) → BatchNorm → ReLU() → MaxPool2D(2,2)
- Conv2D(512→1024, kernel_size=3) → BatchNorm → ReLU()
- Conv2D(1024→1024, kernel_size=3) → BatchNorm → ReLU() → MaxPool2D(2,2)

**Fully Connected Layers:**
- Global Average Pooling
- Linear(1024, 512) → ReLU() → Dropout(0.5)
- Linear(512, 256) → ReLU() → Dropout(0.4)
- Linear(256, 128) → ReLU() → Dropout(0.3)
- Linear(128, 4) (Output Layer with 4 classes: ['glioma', 'meningioma', 'notumor', 'pituitary'])

**Model Statistics:**
- Total Parameters: ~19.3M
- Test Accuracy: ~94.7%

## Installation & Setup

### Clone Repository
```bash
git clone https://github.com/shreyakumari0301/Brain-Tumor-Detection.git
cd Brain-Tumor-Detection
```

### Install Dependencies
Make sure you have Python installed (preferably Python 3.8+), then install the required libraries:

```bash
pip install -r requirements.txt
```

### Model Setup
Ensure the trained model file `best_cnn.pth` is in the `models/` directory. The model file should be ~77 MB.

### Run Application

**Option 1: Start Both Servers (Windows)**
```bash
start_all.bat
```

**Option 2: Manual Start**

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
streamlit run frontend/app.py
```

The backend API will be available at `http://localhost:8000` and the frontend will open at `http://localhost:8501`.

**Note:** If running backend in WSL and frontend in Windows, the frontend will automatically detect and use the WSL IP address.

## Features

✅ Upload MRI Images for classification  
✅ Displays Tumor Type with Confidence Score  
✅ Generates Probability Distribution for all classes  
✅ Provides Descriptive Information about Tumor Type  
✅ Real-time prediction with FastAPI backend  
✅ Modern Streamlit web interface  
✅ Automatic WSL networking support  

## Project Structure

```
BrainTumor/
├── backend/
│   ├── main.py          # FastAPI server
│   └── model_utils.py   # Model architecture and utilities
├── frontend/
│   └── app.py           # Streamlit frontend
├── models/              # Model directory
│   └── best_cnn.pth    # Trained model file (~77 MB)
├── notebook/
│   └── notebook8fc15461ad.ipynb  # Training notebook
├── requirements.txt     # Python dependencies
├── start_backend.bat    # Windows: Start backend
├── start_frontend.bat   # Windows: Start frontend
├── start_all.bat        # Windows: Start both servers
└── README.md
```

## API Endpoints

### Health Check
```
GET /health
```

### Predict Tumor
```
POST /predict
Content-Type: multipart/form-data
Body: image file
```

**Response:**
```json
{
  "prediction": "glioma",
  "has_tumor": true,
  "confidence": 95.23,
  "all_probabilities": {
    "glioma": 0.9523,
    "meningioma": 0.0234,
    "pituitary": 0.0123,
    "notumor": 0.0120
  },
  "message": "Predicted: glioma (95.23% confidence)"
}
```

## Usage

1. Start the backend server (see Installation & Setup)
2. Start the Streamlit frontend
3. Upload a brain MRI image (JPG, JPEG, or PNG)
4. Click "Predict" to analyze the image
5. View the results with:
   - Tumor type classification
   - Confidence score
   - Probability distribution for all classes

## Technical Details

- **Framework:** PyTorch
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Input Size:** 224x224 RGB images
- **Preprocessing:** CLAHE enhancement, thresholding, contour detection, cropping
- **Accuracy:** ~94.7% on test set

## Notes

- The model expects grayscale MRI images (converted to RGB during preprocessing)
- Images are automatically preprocessed using the same pipeline as training
- GPU is recommended for faster inference but CPU will work
- Model file should be in `models/` directory or root directory
- Backend must be running before using the frontend

## License

This project is open source and available for educational purposes.
