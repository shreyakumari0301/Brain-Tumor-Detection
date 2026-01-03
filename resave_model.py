#!/usr/bin/env python3
"""
Re-save model from notebook
Run this in your Jupyter notebook or as a script after training
"""
import torch
from backend.model_utils import UltimateCNN

def resave_model_from_notebook():
    """
    If you have the trained model in memory from your notebook,
    run this to save it properly.
    
    Usage in notebook:
    1. After training completes
    2. Run: resave_model_from_notebook()
    """
    # This assumes you have 'model' variable in scope from training
    # If not, you'll need to load it first
    
    try:
        # Try to get model from global scope (if running in notebook)
        import __main__
        if hasattr(__main__, 'model'):
            model = __main__.model
            print("Found model in global scope")
        else:
            raise AttributeError("Model not found in global scope")
    except:
        print("""
        Model not found. You need to either:
        
        1. Run this in your Jupyter notebook after training:
           torch.save(model.state_dict(), 'best_cnn.pth')
        
        2. Or if you have a working model file elsewhere, load and re-save it
        """)
        return False
    
    # Save the model
    output_path = 'best_cnn.pth'
    print(f"Saving model to {output_path}...")
    torch.save(model.state_dict(), output_path)
    
    # Verify
    file_size = os.path.getsize(output_path)
    print(f"✅ Model saved! Size: {file_size:,} bytes ({file_size / (1024*1024):.2f} MB)")
    
    # Test load
    test = torch.load(output_path, map_location='cpu', weights_only=False)
    print(f"✅ Verified: {len(test)} parameter groups loaded")
    
    return True

if __name__ == "__main__":
    import os
    print("""
    This script is meant to be run in your Jupyter notebook after training.
    
    In your notebook, after training completes, simply run:
    
        torch.save(model.state_dict(), 'best_cnn.pth')
    
    Or if you need to re-save an existing model:
    
        model = UltimateCNN(num_classes=4)
        model.load_state_dict(torch.load('old_model.pth', map_location='cpu', weights_only=False))
        torch.save(model.state_dict(), 'best_cnn.pth')
    """)

