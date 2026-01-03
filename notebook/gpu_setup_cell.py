# Add this cell to your Jupyter notebook to check and enable GPU

import torch
import os

# Check GPU availability
print("=" * 60)
print("GPU Configuration Check")
print("=" * 60)

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"✅ CUDA version: {torch.version.cuda}")
    print(f"✅ GPU device: {torch.cuda.get_device_name(0)}")
    print(f"✅ GPU count: {torch.cuda.device_count()}")
    
    # Show GPU memory
    for i in range(torch.cuda.device_count()):
        props = torch.cuda.get_device_properties(i)
        print(f"   GPU {i}: {props.name} - {props.total_memory / (1024**3):.2f} GB")
    
    device = torch.device('cuda:0')
    print(f"\n✅ Using GPU: {device}")
else:
    print("❌ GPU not available")
    print("\nTo enable GPU:")
    print("1. Install PyTorch with CUDA: pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118")
    print("2. Or use Google Colab/Kaggle (free GPU)")
    device = torch.device('cpu')
    print(f"\n⚠️  Using CPU instead: {device}")

print("=" * 60)

