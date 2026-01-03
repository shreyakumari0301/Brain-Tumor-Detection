#!/bin/bash
# Force remove lock and push all files

cd "/mnt/c/Users/shrey/BrainTumor'" || exit 1

echo "=== Force Push All Files ==="
echo ""

# Aggressively remove lock file
echo "1. Removing lock file..."
for i in {1..5}; do
    rm -rf .git/index.lock
    sleep 0.3
done
echo "   ✅ Lock removed"

# Check for any git processes and kill them
echo ""
echo "2. Checking for git processes..."
pkill -f "git" || true
sleep 1

# Remove lock again
rm -rf .git/index.lock

# Add all files
echo ""
echo "3. Adding all files..."
git add -A

# Verify what's staged
echo ""
echo "4. Staged files:"
git status --short | head -20

# Remove lock before commit
rm -rf .git/index.lock
sleep 0.5

# Commit
echo ""
echo "5. Committing..."
git commit -m "Add complete brain tumor detection system: FastAPI backend, Streamlit frontend, model utilities, documentation, and setup scripts" || {
    echo "   Commit failed, trying again..."
    rm -rf .git/index.lock
    sleep 1
    git commit -m "Add complete brain tumor detection system"
}

# Remove lock before push
rm -rf .git/index.lock
sleep 0.5

# Push
echo ""
echo "6. Pushing to remote..."
git push origin main || {
    echo "   Push failed, pulling first..."
    rm -rf .git/index.lock
    git pull origin main --no-rebase
    rm -rf .git/index.lock
    git push origin main
}

echo ""
echo "=== ✅ Done! Check GitHub ==="

