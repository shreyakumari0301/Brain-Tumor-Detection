#!/bin/bash
# Aggressive fix for lock file and push

cd "/mnt/c/Users/shrey/BrainTumor'" || exit 1

echo "=== Aggressive Git Fix ==="
echo ""

# Step 1: Kill ALL git processes
echo "1. Killing all git processes..."
pkill -9 git || true
pkill -9 git-credential || true
sleep 2

# Step 2: Remove lock file multiple times
echo "2. Removing lock file (multiple attempts)..."
for i in {1..10}; do
    rm -rf .git/index.lock
    rm -f .git/index.lock
    sleep 0.2
done

# Step 3: Verify lock is gone
if [ -f .git/index.lock ]; then
    echo "   ❌ Lock file still exists! Trying chmod..."
    chmod 666 .git/index.lock 2>/dev/null || true
    rm -rf .git/index.lock
    sleep 1
fi

if [ -f .git/index.lock ]; then
    echo "   ❌ Cannot remove lock file. Please:"
    echo "      1. Close all terminals/editors"
    echo "      2. Wait 10 seconds"
    echo "      3. Run: rm -rf .git/index.lock"
    echo "      4. Try again"
    exit 1
fi

echo "   ✅ Lock file removed"

# Step 4: Verify git works
echo ""
echo "3. Testing git..."
rm -rf .git/index.lock
git status > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "   ❌ Git still not working"
    exit 1
fi
echo "   ✅ Git is working"

# Step 5: Set remote
echo ""
echo "4. Setting remote..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/shreyakumari0301/Brain-Tumor-Detection.git
echo "   ✅ Remote set"

# Step 6: Add all files
echo ""
echo "5. Adding all files..."
rm -rf .git/index.lock
sleep 0.5
git add -A
echo "   ✅ Files added"

# Step 7: Show status
echo ""
echo "6. Files to commit:"
git status --short | head -20
echo ""

# Step 8: Commit
echo "7. Committing..."
rm -rf .git/index.lock
sleep 0.5
git commit -m "Initial commit: Complete brain tumor detection system" || {
    echo "   ⚠️  Nothing to commit or commit failed"
    git status
}

# Step 9: Push
echo ""
echo "8. Pushing to GitHub..."
rm -rf .git/index.lock
sleep 0.5
git push -u origin main 2>&1 | tee /tmp/git_push_output.txt

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo ""
    echo "=== ✅ SUCCESS! ==="
    echo "Check: https://github.com/shreyakumari0301/Brain-Tumor-Detection"
else
    echo ""
    echo "=== ⚠️  Push had issues ==="
    echo "Output saved to /tmp/git_push_output.txt"
    echo "You may need to:"
    echo "  git pull origin main --allow-unrelated-histories"
    echo "  git push origin main"
fi

