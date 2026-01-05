"""
Brain Tumor Detection - Streamlit Cloud Deployment
Standalone app that includes model inference (no backend required)
"""
import streamlit as st
import sys
import os
import torch
import cv2
import numpy as np
from PIL import Image
from torchvision import transforms

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from model_utils import UltimateCNN, load_model, preprocess_image, predict

# Page configuration
st.set_page_config(
    page_title="Brain Tumor Detection",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .prediction-box {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .tumor-detected {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
    }
    .no-tumor {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
    }
    </style>
""", unsafe_allow_html=True)

# Load model (cached)
@st.cache_resource
def load_trained_model():
    """Load the trained model"""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Try multiple paths for model
    possible_paths = [
        "models/best_cnn.pth",
        "../models/best_cnn.pth",
        "best_cnn.pth",
        "../best_cnn.pth"
    ]
    
    model_path = None
    for path in possible_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if model_path is None:
        st.error("❌ Model file not found! Please ensure best_cnn.pth is in the models/ directory.")
        return None
    
    try:
        model = load_model(model_path, device=device)
        st.success(f"✅ Model loaded from {model_path}")
        return model, device
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None, None

# Header
st.markdown('<h1 class="main-header">🧠 Brain Tumor Detection System</h1>', unsafe_allow_html=True)

# Load model
model, device = load_trained_model()
if model is None:
    st.stop()

st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📋 Instructions")
    st.markdown("""
    1. Upload a brain MRI image
    2. Click 'Predict' to analyze
    3. View the tumor type and confidence
    """)
    
    st.markdown("---")
    st.header("ℹ️ Tumor Types")
    st.markdown("""
    - **Glioma**: Most common type
    - **Meningioma**: Usually benign
    - **Pituitary**: Pituitary gland tumor
    - **No Tumor**: Healthy brain
    """)

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Upload Image")
    uploaded_file = st.file_uploader(
        "Choose a brain MRI image",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a brain MRI scan image"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width='stretch')
        
        # Predict button
        if st.button("🔬 Predict", type="primary", use_container_width=True):
            with st.spinner("Analyzing image..."):
                try:
                    # Reset file pointer and read image bytes
                    uploaded_file.seek(0)
                    img_bytes = uploaded_file.read()
                    
                    # Validate image bytes
                    if not img_bytes or len(img_bytes) == 0:
                        st.error("❌ Image file is empty or could not be read")
                        st.session_state['prediction'] = None
                    else:
                        # Preprocess image
                        image_tensor = preprocess_image(img_bytes)
                        
                        # Make prediction
                        pred_class, confidence, class_probs = predict(model, image_tensor, device=device)
                        
                        # Store result
                        has_tumor = pred_class != "notumor"
                        st.session_state['prediction'] = {
                            'prediction': pred_class,
                            'has_tumor': has_tumor,
                            'confidence': round(confidence * 100, 2),
                            'all_probabilities': class_probs,
                            'message': f"Predicted: {pred_class} ({confidence*100:.2f}% confidence)"
                        }
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.session_state['prediction'] = None

with col2:
    st.header("📊 Prediction Results")
    
    if 'prediction' in st.session_state and st.session_state['prediction'] is not None:
        result = st.session_state['prediction']
        
        # Main prediction box
        has_tumor = result['has_tumor']
        pred_class = result['prediction']
        confidence = result['confidence']
        
        box_class = "tumor-detected" if has_tumor else "no-tumor"
        tumor_status = "⚠️ TUMOR DETECTED" if has_tumor else "✅ NO TUMOR"
        
        st.markdown(f"""
        <div class="prediction-box {box_class}">
            <h2>{tumor_status}</h2>
            <h3>Type: {pred_class.upper()}</h3>
            <h3>Confidence: {confidence}%</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed probabilities
        st.subheader("📈 Detailed Probabilities")
        probs = result['all_probabilities']
        
        # Sort by probability
        sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
        
        for class_name, prob in sorted_probs:
            prob_percent = prob * 100
            st.progress(prob, text=f"{class_name.capitalize()}: {prob_percent:.2f}%")
        
        # Information box
        st.markdown("---")
        st.info(f"**Result**: {result['message']}")
        
    else:
        st.info("👆 Upload an image and click 'Predict' to see results here")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Brain Tumor Detection System | Powered by Deep Learning</div>",
    unsafe_allow_html=True
)
