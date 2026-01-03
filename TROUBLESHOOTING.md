# Troubleshooting Guide

## Backend Connection Issues

### Error: "Cannot connect to backend API"

**Symptoms:**
- Frontend shows: "❌ Cannot connect to backend API"
- Error message: "Make sure the server is running"

**Solutions:**

#### 1. Check if Backend is Running

```bash
# Test backend connection
python test_backend.py

# Or manually test
curl http://localhost:8000/health
```

#### 2. Start the Backend

**Windows:**
```bash
start_backend.bat
```

**Linux/Mac/WSL:**
```bash
cd backend
python main.py
```

**Using uvicorn directly:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Check Port Availability

**Windows:**
```bash
netstat -ano | findstr :8000
```

**Linux/Mac/WSL:**
```bash
lsof -i :8000
# or
netstat -tuln | grep 8000
```

If port is in use, kill the process or use a different port.

#### 4. WSL-Specific Issues

If you're running in WSL (Windows Subsystem for Linux):

**Problem:** Frontend in Windows can't reach backend in WSL

**Solution 1:** Use WSL hostname
```bash
# In WSL, find your IP
hostname -I

# Update frontend to use WSL IP
# In frontend/app.py or set environment variable:
export BACKEND_URL=http://<WSL_IP>:8000
```

**Solution 2:** Use Windows localhost (WSL2)
```bash
# Backend should bind to 0.0.0.0 (already configured)
# Access from Windows using:
http://localhost:8000
```

**Solution 3:** Run both in same environment
- Run both frontend and backend in WSL, OR
- Run both frontend and backend in Windows

#### 5. Install Missing Dependencies

If you see `python-multipart` error:

```bash
pip install python-multipart
```

Or reinstall all dependencies:

```bash
pip install -r requirements.txt
```

#### 6. Firewall Issues

**Windows:**
- Check Windows Firewall settings
- Allow Python through firewall
- Allow port 8000

**Linux:**
```bash
# Check firewall status
sudo ufw status

# If needed, allow port 8000
sudo ufw allow 8000
```

---

## Model Loading Issues

### Error: "Model file not found"

**Solution:**
1. Ensure `best_cnn.pth` exists in one of these locations:
   - `models/best_cnn.pth` (recommended)
   - Root directory: `best_cnn.pth`
   
2. Or set MODEL_PATH environment variable:
   ```bash
   export MODEL_PATH=/path/to/your/model.pth
   ```

3. Check file permissions:
   ```bash
   ls -la models/best_cnn.pth
   ```

---

## Frontend Issues

### Streamlit Deprecation Warnings

**Fixed in latest version** - `use_container_width` replaced with `width='stretch'`

### Frontend Won't Start

```bash
# Check if Streamlit is installed
pip install streamlit

# Start frontend
streamlit run frontend/app.py
```

### Port 8501 Already in Use

```bash
# Use different port
streamlit run frontend/app.py --server.port 8502
```

---

## Common Error Messages

### "Form data requires python-multipart"

```bash
pip install python-multipart
```

### "CUDA initialization: The NVIDIA driver is too old"

This is a warning, not an error. The system will fall back to CPU. To fix:
- Update NVIDIA drivers
- Or ignore (CPU will work fine)

### "ModuleNotFoundError"

```bash
pip install -r requirements.txt
```

---

## Quick Diagnostic Commands

```bash
# 1. Test backend
python test_backend.py

# 2. Check Python version
python --version  # Should be 3.8+

# 3. Check installed packages
pip list | grep fastapi
pip list | grep streamlit
pip list | grep torch

# 4. Test model loading
python -c "from backend.model_utils import load_model; import torch; model = load_model('models/best_cnn.pth', 'cpu'); print('OK')"

# 5. Check if ports are free
# Windows:
netstat -ano | findstr ":8000 :8501"
# Linux/Mac:
lsof -i :8000 -i :8501
```

---

## Still Having Issues?

1. **Check logs:**
   - Backend logs will show in the terminal where you started it
   - Frontend logs show in the Streamlit interface

2. **Verify environment:**
   - Python 3.8+ required
   - All dependencies installed
   - Model file exists and is accessible

3. **Test components separately:**
   - Test backend API directly: `curl http://localhost:8000/health`
   - Test frontend without backend (will show connection error, but UI should load)

4. **Check file paths:**
   - Ensure you're running commands from the correct directory
   - Use absolute paths if relative paths don't work

