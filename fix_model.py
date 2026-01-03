#!/usr/bin/env python3
"""Attempt to fix/verify and re-save the model file"""
import torch
import os
import sys
from backend.model_utils import UltimateCNN

def fix_model(input_path, output_path=None):
    """Try to load and re-save the model"""
    if output_path is None:
        output_path = input_path.replace('.pth', '_fixed.pth')
    
    print(f"Attempting to fix model: {input_path}")
    print(f"Output will be saved to: {output_path}")
    print("-" * 50)
    
    try:
        # Try to load the corrupted file
        print("Step 1: Loading model file...")
        state_dict = torch.load(input_path, map_location='cpu', weights_only=False)
        print("✅ Successfully loaded state dict!")
        
        # Create model and load state dict
        print("Step 2: Creating model architecture...")
        model = UltimateCNN(num_classes=4)
        
        print("Step 3: Loading weights into model...")
        model.load_state_dict(state_dict)
        print("✅ Successfully loaded weights!")
        
        # Re-save the model properly
        print(f"Step 4: Re-saving model to {output_path}...")
        torch.save(model.state_dict(), output_path)
        print(f"✅ Model re-saved successfully!")
        
        # Verify the new file
        print(f"\nStep 5: Verifying new file...")
        file_size = os.path.getsize(output_path)
        print(f"New file size: {file_size:,} bytes ({file_size / (1024*1024):.2f} MB)")
        
        # Test loading the new file
        test_state_dict = torch.load(output_path, map_location='cpu', weights_only=False)
        test_model = UltimateCNN(num_classes=4)
        test_model.load_state_dict(test_state_dict)
        print("✅ New file verified - can be loaded successfully!")
        
        print(f"\n✅ SUCCESS! Use this file: {output_path}")
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to fix model: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        print("\nThe model file may be too corrupted to fix.")
        print("You may need to retrain the model or restore from a backup.")
        return False

if __name__ == "__main__":
    # Find model file
    possible_paths = [
        "models/best_cnn.pth",
        "best_cnn.pth",
        "../models/best_cnn.pth",
        "../best_cnn.pth"
    ]
    
    input_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    if not input_path:
        for path in possible_paths:
            if os.path.exists(path):
                input_path = path
                break
    
    if not input_path or not os.path.exists(input_path):
        print("❌ Model file not found!")
        print("Please provide the path to best_cnn.pth")
        print("Usage: python fix_model.py <path_to_model.pth>")
        sys.exit(1)
    
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    if output_path is None:
        # Save to models directory if it exists
        if os.path.exists("models"):
            output_path = "models/best_cnn_fixed.pth"
        else:
            output_path = "best_cnn_fixed.pth"
    
    success = fix_model(input_path, output_path)
    sys.exit(0 if success else 1)

