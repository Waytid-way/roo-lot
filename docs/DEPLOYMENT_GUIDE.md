# Deploying to Streamlit Cloud

## Prerequisites
- A GitHub account
- A Streamlit Cloud account (share.streamlit.io)
- The project code pushed to a GitHub repository

## Step-by-Step Guide

### 1. Prepare Repository
Ensure your repository has the following files:
- `app.py`: The main application file.
- `requirements.txt`: List of Python dependencies.
- `.streamlit/config.toml`: Theme configuration (optional).
- `models/`: Directory containing `model_optimized.pkl` and `scaler.pkl`.

### 2. Connect to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repository (`roo-lot`)
4. Select the branch (`main` or `master`)
5. select `app.py` as the main file path.

### 3. Deploy
1. Click "Deploy!"
2. Wait for the build to complete (installing requirements).
3. Once deployed, your app will be live at `https://your-app-name.streamlit.app`.

## Troubleshooting

### "ModuleNotFoundError"
- Check that the missing module is listed in `requirements.txt`.

### "FileNotFoundError: models/..."
- Ensure the `models/` directory is committed and pushed to GitHub.
- Check `.gitignore` to make sure `.pkl` files are NOT ignored (remove `*.pkl` if present, or force add them).

**IMPORTANT:** The current `.gitignore` ignores `*.pkl`. You MUST force add the model files before deploying:
```bash
git add -f models/model_optimized.pkl models/scaler.pkl models/model_metadata.json
git commit -m "Force add model artifacts for deployment"
git push origin master
```
