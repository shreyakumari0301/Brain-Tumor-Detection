#!/bin/bash
# Add all files and push to remote

cd "/mnt/c/Users/shrey/BrainTumor'" || exit 1

echo "=== Adding All Files and Pushing ==="
echo ""

# Remove lock file
rm -f .git/index.lock

# Check what will be added
echo "Files to be added:"
git status --short
echo ""

# Add all files (including untracked)
echo "Adding all files..."
rm -f .git/index.lock
git add -A

# Show what's staged
echo ""
echo "Staged files:"
git status --short
echo ""

# Commit
echo "Committing..."
rm -f .git/index.lock
git commit -m "Add complete brain tumor detection system: backend (FastAPI), frontend (Streamlit), model utilities, and documentation" || {
    echo "No changes to commit or commit failed"
}

# Push
echo ""
echo "Pushing to remote..."
rm -f .git/index.lock
git push origin main || {
    echo ""
    echo "Push failed. Trying to pull first..."
    rm -f .git/index.lock
    git pull origin main --no-rebase || {
        echo "Pull also failed. You may need to resolve conflicts manually."
        exit 1
    }
    echo "Pull successful. Pushing again..."
    rm -f .git/index.lock
    git push origin main
}

echo ""
echo "=== Done! Check your GitHub repository ==="

