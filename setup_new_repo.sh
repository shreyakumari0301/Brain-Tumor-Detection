#!/bin/bash
# Setup and push to new repository

cd "/mnt/c/Users/shrey/BrainTumor'" || exit 1

echo "=== Setting Up New Repository ==="
echo ""

# Step 1: Remove lock file
echo "1. Removing lock file..."
rm -rf .git/index.lock
sleep 1
echo "   ✅ Lock removed"

# Step 2: Check/Set remote
echo ""
echo "2. Checking remote..."
CURRENT_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
EXPECTED_REMOTE="https://github.com/shreyakumari0301/Brain-Tumor-Detection.git"

if [ "$CURRENT_REMOTE" != "$EXPECTED_REMOTE" ]; then
    echo "   Setting remote to: $EXPECTED_REMOTE"
    git remote remove origin 2>/dev/null || true
    git remote add origin "$EXPECTED_REMOTE"
else
    echo "   ✅ Remote already set correctly"
fi

# Step 3: Add all files
echo ""
echo "3. Adding all files..."
rm -rf .git/index.lock
git add -A

# Step 4: Show what will be committed
echo ""
echo "4. Files to be committed:"
git status --short | head -30
echo ""

# Step 5: Commit
echo "5. Committing..."
rm -rf .git/index.lock
git commit -m "Initial commit: Complete brain tumor detection system

- FastAPI backend with model inference
- Streamlit frontend for image upload and prediction
- Model utilities and preprocessing pipeline
- Complete documentation and setup guides
- Training notebook
- Requirements and configuration files" || {
    echo "   ⚠️  Commit failed or nothing to commit"
}

# Step 6: Push to new repository
echo ""
echo "6. Pushing to new repository..."
rm -rf .git/index.lock

# Check if this is the first push
if git ls-remote --heads origin main 2>/dev/null | grep -q main; then
    echo "   Remote branch exists, pushing normally..."
    git push origin main || git push -u origin main
else
    echo "   First push to new repository..."
    git push -u origin main
fi

echo ""
echo "=== ✅ Done! Check your GitHub repository ==="
echo "Repository: https://github.com/shreyakumari0301/Brain-Tumor-Detection"

