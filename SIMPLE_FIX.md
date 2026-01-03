# Simple Fix for Git Lock File Issue

## Quick Solution

Run these commands **one at a time** in WSL:

```bash
cd "/mnt/c/Users/shrey/BrainTumor'"

# 1. Kill all git processes
pkill -9 git
sleep 3

# 2. Remove lock file
rm -rf .git/index.lock
rm -f .git/index.lock

# 3. Wait a moment
sleep 2

# 4. Verify git works
git status

# 5. If git status works, continue:
git remote set-url origin https://github.com/shreyakumari0301/Brain-Tumor-Detection.git

# 6. Add files
git add -A

# 7. Commit
git commit -m "Initial commit: Complete brain tumor detection system"

# 8. Push
git push -u origin main
```

## If Lock File Keeps Appearing

1. **Close ALL terminals and editors** (VS Code, Cursor, etc.)
2. **Wait 10 seconds**
3. **Open ONE new terminal**
4. **Run the commands above**

## Alternative: Use GitHub Desktop or VS Code Git

If command line keeps failing:
1. Open VS Code or GitHub Desktop
2. Add all files
3. Commit
4. Push

This avoids the lock file issue.

