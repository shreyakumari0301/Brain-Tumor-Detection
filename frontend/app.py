import streamlit as st
import requests
import io
from PIL import Image
import os

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

# Backend API URL
# Default to localhost, but can be overridden for WSL
# If backend is in WSL, use WSL IP: http://172.24.173.114:8000
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Try WSL IP if localhost doesn't work (for WSL2)
WSL_IP = "172.24.173.114"  # Update this if your WSL IP changes
WSL_BACKEND_URL = f"http://{WSL_IP}:8000"

# Check backend connection on startup
@st.cache_data(ttl=10)
def check_backend_connection():
    """Check if backend is accessible"""
    # Try default URL first
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, response.json(), BACKEND_URL
    except:
        pass
    
    # If localhost fails, try WSL IP (for WSL2)
    try:
        response = requests.get(f"{WSL_BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, response.json(), WSL_BACKEND_URL
    except:
        pass
    
    return False, None, None

# Header
st.markdown('<h1 class="main-header">🧠 Brain Tumor Detection System</h1>', unsafe_allow_html=True)

# Backend status indicator
backend_ok, backend_info, active_url = check_backend_connection()
if not backend_ok:
    st.error("⚠️ **Backend API is not accessible!** Please start the backend server first.")
    with st.expander("How to start the backend"):
        st.code("""
# Option 1: Using the batch file (Windows)
start_backend.bat

# Option 2: Manual start
cd backend
python main.py

# Option 3: Using uvicorn directly
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
        """, language="bash")
        st.info(f"Backend should be running at: `{BACKEND_URL}`")
        
        # WSL networking help
        st.warning("""
        **If backend is running in WSL:**
        - Make sure backend binds to `0.0.0.0` (already configured)
        - Try accessing from Windows using `localhost:8000`
        - If that doesn't work, find WSL IP: `hostname -I` in WSL
        - Then set BACKEND_URL environment variable to that IP
        """)
else:
    # Update BACKEND_URL if we're using WSL IP
    if active_url and active_url != BACKEND_URL:
        BACKEND_URL = active_url
    st.success(f"✅ Backend connected: {BACKEND_URL}")
    if backend_info:
        st.json(backend_info)

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
    
    st.markdown("---")
    st.text(f"Backend URL: {BACKEND_URL}")
    if st.button("🔍 Check API Status"):
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                st.success(f"✅ API is running")
                st.json(data)
            else:
                st.error(f"❌ API returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API")
            st.info("Make sure the backend is running:\n```bash\ncd backend\npython main.py\n```")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

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
                        # Send to backend
                        files = {"image": (uploaded_file.name, img_bytes, uploaded_file.type)}
                        response = requests.post(f"{BACKEND_URL}/predict", files=files, timeout=30)
                    
                        if response.status_code == 200:
                            result = response.json()
                            st.session_state['prediction'] = result
                        else:
                            error_detail = "Unknown error"
                            try:
                                error_detail = response.json().get('detail', 'Unknown error')
                            except:
                                error_detail = response.text[:200]
                            st.error(f"❌ Error: {error_detail}")
                            st.session_state['prediction'] = None
                
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend API. Make sure the server is running.")
                    st.info(f"**Expected API URL**: `{BACKEND_URL}`")
                    st.code("cd backend\npython main.py", language="bash")
                    st.warning("💡 If running in WSL, make sure the backend is accessible on the correct host/port.")
                    st.session_state['prediction'] = None
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

