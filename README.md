# Brain Tumor Detection System

A full-stack application for detecting brain tumors from MRI images using deep learning. The system consists of a FastAPI backend and a Streamlit frontend.

## Features

- 🧠 Classifies brain MRI images into 4 categories:
  - **Glioma** - Most common type
  - **Meningioma** - Usually benign
  - **Pituitary** - Pituitary gland tumor
  - **No Tumor** - Healthy brain
- 📊 Shows confidence scores and detailed probabilities
- 🎨 Modern, user-friendly interface
- ⚡ Fast inference with PyTorch

## Project Structure

```
BrainTumor/
├── backend/
│   ├── main.py          # FastAPI server
│   └── model_utils.py   # Model architecture and utilities
├── frontend/
│   └── app.py           # Streamlit frontend
├── models/              # Model directory
│   └── best_cnn.pth    # Trained model file
├── notebook/
│   └── notebook8fc15461ad.ipynb  # Training notebook
├── requirements.txt     # Python dependencies
├── start_backend.bat    # Windows: Start backend
├── start_frontend.bat   # Windows: Start frontend
├── start_all.bat        # Windows: Start both servers
└── README.md
```

---

## 📋 All Commands

### 1. Installation Commands

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Install Specific Packages (if needed)
```bash
pip install fastapi uvicorn streamlit torch torchvision opencv-python pillow numpy requests
```

#### Verify Installation
```bash
python --version
pip list | grep fastapi
pip list | grep streamlit
```

---

### 2. Model Setup Commands

#### Check if model file exists
```bash
# Windows
dir best_cnn.pth
dir models\best_cnn.pth

# Linux/Mac
ls best_cnn.pth
ls models/best_cnn.pth
```

#### Move model to models directory (if needed)
```bash
# Windows
mkdir models
copy best_cnn.pth models\best_cnn.pth

# Linux/Mac
mkdir -p models
cp best_cnn.pth models/best_cnn.pth
```

#### Set custom model path (optional)
```bash
# Windows
set MODEL_PATH=path\to\your\model.pth

# Linux/Mac
export MODEL_PATH=/path/to/your/model.pth
```

---

### 3. Backend Server Commands

#### Start Backend (Method 1 - Using main.py)
```bash
cd backend
python main.py
```

#### Start Backend (Method 2 - Using uvicorn directly)
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Start Backend (Method 3 - Windows batch file)
```bash
start_backend.bat
```

#### Start Backend (Method 4 - Production mode)
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Test Backend Health
```bash
# Using curl
curl http://localhost:8000/health

# Using PowerShell (Windows)
Invoke-WebRequest -Uri http://localhost:8000/health

# Using Python
python -c "import requests; print(requests.get('http://localhost:8000/health').json())"
```

#### Test Backend Prediction (via API)
```bash
# Using curl
curl -X POST "http://localhost:8000/predict" -F "image=@path/to/image.jpg"

# Using Python
python -c "import requests; files={'image': open('image.jpg', 'rb')}; print(requests.post('http://localhost:8000/predict', files=files).json())"
```

---

### 4. Frontend Server Commands

#### Start Frontend (Method 1 - Standard)
```bash
streamlit run frontend/app.py
```

#### Start Frontend (Method 2 - Windows batch file)
```bash
start_frontend.bat
```

#### Start Frontend (Method 3 - Custom port)
```bash
streamlit run frontend/app.py --server.port 8502
```

#### Start Frontend (Method 4 - Custom backend URL)
```bash
# Windows
set BACKEND_URL=http://localhost:8000
streamlit run frontend/app.py

# Linux/Mac
export BACKEND_URL=http://localhost:8000
streamlit run frontend/app.py
```

---

### 5. Start Both Servers Commands

#### Windows - Start Both (Method 1)
```bash
start_all.bat
```

#### Windows - Start Both (Method 2 - Manual)
```bash
# Terminal 1
cd backend
python main.py

# Terminal 2 (new terminal)
streamlit run frontend/app.py
```

#### Linux/Mac - Start Both
```bash
# Terminal 1
cd backend
python main.py &

# Terminal 2
streamlit run frontend/app.py
```

#### Linux/Mac - Start Both (with nohup)
```bash
# Terminal 1
cd backend
nohup python main.py > backend.log 2>&1 &

# Terminal 2
nohup streamlit run frontend/app.py > frontend.log 2>&1 &
```

---

### 6. Testing Commands

#### Test Backend API
```bash
# Health check
curl http://localhost:8000/health

# Root endpoint
curl http://localhost:8000/

# Prediction (replace with actual image path)
curl -X POST http://localhost:8000/predict -F "image=@test_image.jpg"
```

#### Test Frontend Connection
```bash
# Check if frontend can reach backend
python -c "import requests; r = requests.get('http://localhost:8000/health'); print('Connected!' if r.status_code == 200 else 'Failed')"
```

#### Test Model Loading
```bash
python -c "from backend.model_utils import load_model; import torch; model = load_model('models/best_cnn.pth', 'cpu'); print('Model loaded successfully!')"
```

---

### 7. Development Commands

#### Run with Auto-reload (Backend)
```bash
cd backend
uvicorn main:app --reload
```

#### Run with Auto-reload (Frontend)
```bash
streamlit run frontend/app.py --server.runOnSave true
```

#### Check Python Version
```bash
python --version
```

#### Check Installed Packages
```bash
pip list
```

#### Update Packages
```bash
pip install --upgrade -r requirements.txt
```

---

### 8. Troubleshooting Commands

#### Check if ports are in use
```bash
# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :8501

# Linux/Mac
lsof -i :8000
lsof -i :8501
```

#### Kill process on port (if needed)
```bash
# Windows (replace PID with actual process ID)
taskkill /PID <PID> /F

# Linux/Mac
kill -9 $(lsof -t -i:8000)
kill -9 $(lsof -t -i:8501)
```

#### Check GPU availability (for PyTorch)
```bash
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"CPU\"}')"
```

#### Verify model file integrity
```bash
python -c "import torch; model = torch.load('models/best_cnn.pth', map_location='cpu'); print('Model loaded successfully'); print(f'Keys: {len(model.keys())}')"
```

---

### 9. Access URLs

Once servers are running:

- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **API Health**: http://localhost:8000/health

---

## 🚀 Quick Start Guide

### Windows Users

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start both servers:**
   ```bash
   start_all.bat
   ```

3. **Open browser** to http://localhost:8501

### Linux/Mac Users

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start backend (Terminal 1):**
   ```bash
   cd backend
   python main.py
   ```

3. **Start frontend (Terminal 2):**
   ```bash
   streamlit run frontend/app.py
   ```

4. **Open browser** to http://localhost:8501

---

## 📡 API Endpoints

### Health Check
```bash
GET http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### Predict Tumor
```bash
POST http://localhost:8000/predict
Content-Type: multipart/form-data
Body: image file
```

Response:
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

---

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_PATH` | Path to model file | `models/best_cnn.pth` |
| `BACKEND_URL` | Backend API URL | `http://localhost:8000` |

### Set Environment Variables

**Windows:**
```bash
set MODEL_PATH=path\to\model.pth
set BACKEND_URL=http://localhost:8000
```

**Linux/Mac:**
```bash
export MODEL_PATH=/path/to/model.pth
export BACKEND_URL=http://localhost:8000
```

---

## 📝 Usage Instructions

1. **Start the backend server** (see commands above)
2. **Start the frontend server** (see commands above)
3. **Open the Streamlit UI** at http://localhost:8501
4. **Upload a brain MRI image** (JPG, JPEG, or PNG)
5. **Click "Predict"** to analyze the image
6. **View results:**
   - Tumor type classification
   - Confidence score
   - Probability distribution for all classes

---

## ⚙️ Technical Details

- **Model Architecture**: Custom CNN (UltimateCNN) with ~19M parameters
- **Input Size**: 224x224 RGB images
- **Preprocessing**: CLAHE enhancement, thresholding, contour detection, cropping
- **Accuracy**: ~94.7% on test set
- **Framework**: PyTorch
- **Backend**: FastAPI
- **Frontend**: Streamlit

---

## 📌 Notes

- The model expects grayscale MRI images (converted to RGB during preprocessing)
- Images are automatically preprocessed using the same pipeline as training
- GPU is recommended for faster inference but CPU will work
- Model file should be in `models/` directory or root directory
- Backend must be running before using the frontend

---

## 🐛 Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Verify model file exists and is accessible
- Check Python version (3.8+ required)

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check `BACKEND_URL` environment variable
- Verify firewall settings

### Model not loading
- Verify model file path is correct
- Check file permissions
- Ensure model file is not corrupted

### Prediction errors
- Verify image format (JPG, JPEG, PNG)
- Check image is a valid brain MRI scan
- Ensure backend logs for detailed error messages

---

## 📚 Additional Resources

- Training notebook: `notebook/notebook8fc15461ad.ipynb`
- API documentation: http://localhost:8000/docs (when backend is running)
- FastAPI docs: https://fastapi.tiangolo.com/
- Streamlit docs: https://docs.streamlit.io/
