# Quick Push All Files to GitHub

Run these commands in WSL:

```bash
cd "/mnt/c/Users/shrey/BrainTumor'"

# Remove lock file
rm -f .git/index.lock

# Add ALL files (including new ones)
git add -A

# Check what will be committed
git status

# Commit everything
git commit -m "Add complete brain tumor detection system: FastAPI backend, Streamlit frontend, model utilities, and documentation"

# Push to remote
rm -f .git/index.lock
git push origin main
```

If push fails due to remote changes:

```bash
# Pull first
rm -f .git/index.lock
git pull origin main --no-rebase

# Then push again
rm -f .git/index.lock
git push origin main
```

## Files that should be pushed:

- ✅ `backend/` - FastAPI backend
- ✅ `frontend/` - Streamlit frontend  
- ✅ `models/` - Model directory (if you want to track the .pth file)
- ✅ `notebook/` - Training notebook
- ✅ `requirements.txt` - Dependencies
- ✅ `README.md` - Documentation
- ✅ All other project files

## Note about model file:

The `best_cnn.pth` file is ~77 MB. GitHub has a 100 MB file size limit. If you want to exclude it:

1. Add to `.gitignore`: `models/*.pth`
2. Or use Git LFS for large files
3. Or document where to download it instead

