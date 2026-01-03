#!/usr/bin/env python3
"""Quick script to check GPU availability and setup"""
import sys

def check_gpu():
    """Check if GPU is available and configured correctly"""
    print("=" * 60)
    print("GPU Availability Check")
    print("=" * 60)
    
    try:
        import torch
        print(f"✅ PyTorch installed: {torch.__version__}")
    except ImportError:
        print("❌ PyTorch not installed")
        print("   Install with: pip install torch torchvision")
        return False
    
    # Check CUDA
    cuda_available = torch.cuda.is_available()
    print(f"\nCUDA Available: {cuda_available}")
    
    if cuda_available:
        print(f"✅ CUDA Version: {torch.version.cuda}")
        print(f"✅ cuDNN Version: {torch.backends.cudnn.version()}")
        print(f"✅ GPU Device: {torch.cuda.get_device_name(0)}")
        print(f"✅ GPU Count: {torch.cuda.device_count()}")
        
        # Check memory
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            print(f"\nGPU {i} Details:")
            print(f"   Name: {props.name}")
            print(f"   Memory: {props.total_memory / (1024**3):.2f} GB")
            print(f"   Compute Capability: {props.major}.{props.minor}")
        
        # Test GPU computation
        print("\n🧪 Testing GPU computation...")
        try:
            x = torch.randn(1000, 1000).cuda()
            y = torch.randn(1000, 1000).cuda()
            z = torch.matmul(x, y)
            print("✅ GPU computation test passed!")
        except Exception as e:
            print(f"❌ GPU computation test failed: {e}")
            return False
        
        print("\n✅ GPU is ready to use!")
        print("\nYour notebook will automatically use GPU.")
        return True
    else:
        print("\n⚠️  GPU not available")
        print("\nPossible reasons:")
        print("   1. No NVIDIA GPU installed")
        print("   2. NVIDIA drivers not installed/updated")
        print("   3. PyTorch installed without CUDA support")
        print("\nTo install PyTorch with CUDA:")
        print("   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118")
        print("\nOr use cloud GPU (Google Colab, Kaggle)")
        return False

if __name__ == "__main__":
    success = check_gpu()
    sys.exit(0 if success else 1)

