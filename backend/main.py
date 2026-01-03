from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import torch
from model_utils import load_model, preprocess_image, predict
import os

# Global model variable
model = None
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler for startup and shutdown"""
    # Startup
    global model
    # Try multiple possible paths
    possible_paths = [
        os.getenv("MODEL_PATH"),
        "../models/best_cnn.pth",
        "models/best_cnn.pth",
        "../best_cnn.pth",
        "best_cnn.pth"
    ]
    
    model_path = None
    for path in possible_paths:
        if path and os.path.exists(path):
            model_path = path
            break
    
    if model_path is None:
        raise FileNotFoundError(
            f"Model file not found. Tried: {possible_paths}. "
            "Please ensure best_cnn.pth is in the models/ directory or root directory."
        )
    
    model = load_model(model_path, device=device)
    print(f"✅ Model loaded successfully from {model_path} on {device}")
    
    yield
    
    # Shutdown (if needed)
    # Cleanup code can go here

app = FastAPI(title="Brain Tumor Detection API", lifespan=lifespan)

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Brain Tumor Detection API", "status": "running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}


@app.post("/predict")
async def predict_tumor(image: UploadFile = File(...)):
    """Predict brain tumor type from uploaded image"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Validate file type
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image bytes
        image_bytes = await image.read()
        
        # Validate image bytes
        if not image_bytes or len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Image file is empty")
        
        # Reset file pointer (in case it was read before)
        await image.seek(0)
        image_bytes = await image.read()
        
        # Preprocess image
        image_tensor = preprocess_image(image_bytes)
        
        # Make prediction
        pred_class, confidence, class_probs = predict(model, image_tensor, device=device)
        
        # Determine if tumor is present
        has_tumor = pred_class != "notumor"
        
        return JSONResponse({
            "prediction": pred_class,
            "has_tumor": has_tumor,
            "confidence": round(confidence * 100, 2),
            "all_probabilities": class_probs,
            "message": f"Predicted: {pred_class} ({confidence*100:.2f}% confidence)"
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

