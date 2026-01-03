#!/usr/bin/env python3
"""Verify if the model file is valid"""
import os
import torch
import sys

def verify_model_file(model_path):
    """Verify if model file is valid"""
    print(f"Checking model file: {model_path}")
    print("-" * 50)
    
    # Check if file exists
    if not os.path.exists(model_path):
        print(f"❌ File not found: {model_path}")
        return False
    
    # Check file size
    file_size = os.path.getsize(model_path)
    print(f"File size: {file_size:,} bytes ({file_size / (1024*1024):.2f} MB)")
    
    if file_size == 0:
        print("❌ File is empty!")
        return False
    
    if file_size < 1000:
        print("⚠️  Warning: File seems too small for a model (expected > 1MB)")
    
    # Check file type
    with open(model_path, 'rb') as f:
        first_bytes = f.read(16)
        print(f"First 16 bytes (hex): {first_bytes.hex()}")
        
        # Check if it looks like text
        try:
            text_preview = first_bytes.decode('utf-8', errors='ignore')
            if text_preview.isprintable() and not any(c in text_preview for c in ['\x00', '\x01', '\x02']):
                print("❌ File appears to be text, not a binary PyTorch file!")
                print(f"   Preview: {text_preview[:50]}...")
                return False
        except:
            pass
    
    # Try to load it
    print("\nAttempting to load model...")
    try:
        state_dict = torch.load(model_path, map_location='cpu', weights_only=False)
        print("✅ Successfully loaded state dict!")
        
        # Check structure
        if isinstance(state_dict, dict):
            print(f"✅ State dict contains {len(state_dict)} keys")
            total_params = sum(p.numel() for p in state_dict.values() if hasattr(p, 'numel'))
            print(f"✅ Total parameters: {total_params:,}")
            
            # Show some keys
            print("\nSample keys:")
            for i, key in enumerate(list(state_dict.keys())[:5]):
                print(f"   - {key}")
            if len(state_dict) > 5:
                print(f"   ... and {len(state_dict) - 5} more")
        else:
            print("⚠️  Warning: State dict is not a dictionary")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to load model: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    # Check multiple possible locations
    possible_paths = [
        "models/best_cnn.pth",
        "best_cnn.pth",
        "../models/best_cnn.pth",
        "../best_cnn.pth"
    ]
    
    model_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    if model_path:
        possible_paths = [model_path] + possible_paths
    
    found = False
    for path in possible_paths:
        if os.path.exists(path):
            print(f"\n{'='*50}")
            found = True
            if verify_model_file(path):
                print(f"\n✅ Model file is valid: {path}")
                sys.exit(0)
            else:
                print(f"\n❌ Model file is invalid: {path}")
                sys.exit(1)
    
    if not found:
        print("❌ Model file not found in any of these locations:")
        for path in possible_paths:
            print(f"   - {path}")
        sys.exit(1)

