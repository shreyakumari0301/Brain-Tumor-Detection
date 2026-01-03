#!/bin/bash
# Fix git lock file and sync with remote

cd "/mnt/c/Users/shrey/BrainTumor'" || exit 1

echo "Step 1: Removing git lock file..."
rm -f .git/index.lock
if [ -f .git/index.lock ]; then
    echo "❌ Lock file still exists"
    exit 1
else
    echo "✅ Lock file removed"
fi

echo ""
echo "Step 2: Checking git status..."
git status --short

echo ""
echo "Step 3: Pulling remote changes..."
git pull origin main --no-rebase

echo ""
echo "Step 4: Adding changes..."
git add .

echo ""
echo "Step 5: Committing..."
git commit -m "Add brain tumor detection system with backend and frontend"

echo ""
echo "Step 6: Pushing to remote..."
git push origin main

echo ""
echo "✅ Done!"

