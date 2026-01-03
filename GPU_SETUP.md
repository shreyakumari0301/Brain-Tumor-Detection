# GPU Setup Guide for Cursor/Jupyter Notebooks

## Quick Check: Is GPU Available?

Run this in a notebook cell to check:

```python
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"GPU device: {torch.cuda.get_device_name(0)}")
    print(f"GPU count: {torch.cuda.device_count()}")
else:
    print("❌ GPU not available - will use CPU")
```

## Option 1: Local GPU Setup (NVIDIA GPU)

### Step 1: Install PyTorch with CUDA

**Check your CUDA version:**
```bash
nvidia-smi
```

**Install PyTorch with CUDA:**

For CUDA 11.8:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

For CUDA 12.1:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

For latest stable:
```bash
pip install torch torchvision torchaudio
```

### Step 2: Verify Installation

```python
import torch
assert torch.cuda.is_available(), "CUDA not available!"
print("✅ GPU is ready!")
```

## Option 2: Use Cloud GPU (Recommended for Training)

### Google Colab (Free GPU)

1. Upload your notebook to Google Colab
2. Go to **Runtime → Change runtime type**
3. Select **GPU** as hardware accelerator
4. Run your notebook

### Kaggle (Free GPU)

1. Upload notebook to Kaggle
2. In notebook settings, enable **GPU**
3. Save and run

### Other Options
- **Paperspace Gradient** - Free GPU tier
- **AWS SageMaker** - Pay per use
- **Azure ML** - Free tier available

## Option 3: Configure Cursor/Jupyter for GPU

### If Using Jupyter in Cursor:

1. **Install Jupyter extension** (if not already installed)
2. **Select kernel** with GPU support:
   - Click kernel selector (top right)
   - Choose environment with PyTorch + CUDA installed

### If Using VS Code Jupyter:

1. Open Command Palette (`Ctrl+Shift+P`)
2. Type: "Python: Select Interpreter"
3. Choose environment with GPU-enabled PyTorch

## Update Your Notebook Code

Your notebook already has GPU detection. Make sure this cell runs first:

```python
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

if torch.cuda.is_available():
    print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
    print(f"✅ CUDA Version: {torch.version.cuda}")
else:
    print("⚠️  Using CPU (slower)")
```

## Force GPU Usage (if available)

If you want to explicitly use GPU:

```python
import torch

# Force GPU if available
if torch.cuda.is_available():
    device = torch.device('cuda:0')  # Use first GPU
    print(f"✅ Using GPU: {torch.cuda.get_device_name(0)}")
else:
    device = torch.device('cpu')
    print("⚠️  GPU not available, using CPU")
```

## Troubleshooting

### "CUDA out of memory" Error

```python
# Clear GPU cache
torch.cuda.empty_cache()

# Use smaller batch size
batch_size = 16  # Instead of 32

# Use gradient accumulation
accumulation_steps = 2
```

### "CUDA driver version is insufficient"

Update your NVIDIA drivers:
- Windows: Download from nvidia.com
- Linux: `sudo apt update && sudo apt install nvidia-driver-xxx`

### Check GPU Memory

```python
if torch.cuda.is_available():
    print(f"GPU Memory Allocated: {torch.cuda.memory_allocated(0) / 1024**3:.2f} GB")
    print(f"GPU Memory Cached: {torch.cuda.memory_reserved(0) / 1024**3:.2f} GB")
```

## Quick Test Cell

Add this to your notebook to test GPU:

```python
import torch

# Test GPU
if torch.cuda.is_available():
    x = torch.randn(1000, 1000).cuda()
    y = torch.randn(1000, 1000).cuda()
    z = torch.matmul(x, y)
    print("✅ GPU test passed!")
    print(f"Device: {x.device}")
else:
    print("❌ GPU not available")
    print("Using CPU instead")
```

## For Your Specific Notebook

Your training code already uses:
```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
```

This will automatically use GPU if available. Just make sure:
1. ✅ PyTorch with CUDA is installed
2. ✅ NVIDIA drivers are up to date
3. ✅ GPU is detected (run the check cell above)

