#!/bin/bash
# Fix git lock and sync properly

cd "/mnt/c/Users/shrey/BrainTumor'" || exit 1

echo "=========================================="
echo "Fixing Git Issues"
echo "=========================================="

# Step 1: Remove lock file forcefully
echo ""
echo "Step 1: Removing git lock file..."
rm -f .git/index.lock
sleep 1
if [ -f .git/index.lock ]; then
    echo "❌ Lock file still exists, trying force remove..."
    rm -rf .git/index.lock
    sleep 1
fi

if [ -f .git/index.lock ]; then
    echo "❌ Cannot remove lock file. Please close any git processes and try again."
    exit 1
else
    echo "✅ Lock file removed"
fi

# Step 2: Check status
echo ""
echo "Step 2: Checking git status..."
git status --short | head -20

# Step 3: Stash any uncommitted changes
echo ""
echo "Step 3: Stashing uncommitted changes..."
git stash

# Step 4: Pull remote changes
echo ""
echo "Step 4: Pulling remote changes..."
rm -f .git/index.lock
git pull origin main --no-edit

# Step 5: Apply stashed changes
echo ""
echo "Step 5: Applying stashed changes..."
git stash pop || true

# Step 6: Add all changes
echo ""
echo "Step 6: Adding changes..."
rm -f .git/index.lock
git add .

# Step 7: Commit
echo ""
echo "Step 7: Committing..."
rm -f .git/index.lock
git commit -m "Add brain tumor detection system with backend and frontend" || echo "No changes to commit"

# Step 8: Push
echo ""
echo "Step 8: Pushing to remote..."
rm -f .git/index.lock
git push origin main

echo ""
echo "=========================================="
echo "✅ Done!"
echo "=========================================="

