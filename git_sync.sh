#!/bin/bash
set -e

cd "/mnt/c/Users/shrey/BrainTumor'" || exit 1

echo "=== Fixing Git Lock and Syncing ==="
echo ""

# Remove lock file multiple times to be sure
echo "1. Removing lock file..."
for i in {1..3}; do
    rm -f .git/index.lock
    sleep 0.5
done

if [ -f .git/index.lock ]; then
    echo "ERROR: Lock file persists. Close all git processes."
    exit 1
fi
echo "   ✅ Lock removed"

# Stash changes
echo ""
echo "2. Stashing local changes..."
git stash push -m "temp_stash_$(date +%s)" || echo "   (no changes to stash)"

# Pull with rebase
echo ""
echo "3. Pulling remote changes..."
rm -f .git/index.lock
git pull origin main --no-rebase || {
    echo "   ⚠️  Pull had issues, trying merge strategy..."
    rm -f .git/index.lock
    git pull origin main --no-edit || true
}

# Restore stashed changes
echo ""
echo "4. Restoring local changes..."
git stash pop || echo "   (no stashed changes)"

# Add and commit
echo ""
echo "5. Adding and committing..."
rm -f .git/index.lock
git add . || true

rm -f .git/index.lock
if git diff --cached --quiet; then
    echo "   (no changes to commit)"
else
    git commit -m "Add brain tumor detection system with backend and frontend" || true
fi

# Push
echo ""
echo "6. Pushing to remote..."
rm -f .git/index.lock
git push origin main || {
    echo "   ⚠️  Push failed, trying with force (use with caution)..."
    read -p "   Force push? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -f .git/index.lock
        git push origin main --force
    fi
}

echo ""
echo "=== Done ==="

