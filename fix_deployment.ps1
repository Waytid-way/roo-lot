# Fix Streamlit Model Deployment Issue
# This script will:
# 1. Check if model files exist
# 2. Force add model files to git (even if in .gitignore)
# 3. Commit and push to GitHub
# 4. Provide deployment instructions

Set-Location "C:\Users\com\Documents\AIE322\RooLord\roo-lot"

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🔧 Fixing Streamlit Model Deployment Issue" -ForegroundColor Yellow
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Step 1: Check model files
Write-Host "Step 1: Checking model files..." -ForegroundColor Green
$modelFiles = @(
    "models/electricbills_predict.pkl",
    "models/model_metadata.json"
)

$allExist = $true
foreach ($file in $modelFiles) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length / 1KB
        Write-Host "  ✓ Found: $file ($([math]::Round($size, 2)) KB)" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Missing: $file" -ForegroundColor Red
        $allExist = $false
    }
}
Write-Host ""

if (-not $allExist) {
    Write-Host "❌ Some model files are missing!" -ForegroundColor Red
    Write-Host "   You need to train the model first." -ForegroundColor Yellow
    Write-Host "   Run: python scripts/train_model.py" -ForegroundColor Cyan
    exit 1
}

# Step 2: Force add model files to git
Write-Host "Step 2: Adding model files to git (forcing ignore rules)..." -ForegroundColor Green
git add -f models/electricbills_predict.pkl
git add -f models/model_metadata.json

# Check if files were added
$status = git status --short
if ($status -match "models/") {
    Write-Host "  ✓ Model files staged successfully" -ForegroundColor Green
} else {
    Write-Host "  ℹ No new changes (model files might already be committed)" -ForegroundColor Yellow
}
Write-Host ""

# Step 3: Commit changes
Write-Host "Step 3: Committing changes..." -ForegroundColor Green
$commitMsg = "Fix: Add model files for Streamlit deployment (Python 3.12.10)"
git commit -m $commitMsg 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Changes committed successfully" -ForegroundColor Green
} else {
    Write-Host "  ℹ No changes to commit (already up to date)" -ForegroundColor Yellow
}
Write-Host ""

# Step 4: Push to GitHub
Write-Host "Step 4: Pushing to GitHub..." -ForegroundColor Green
git push origin master 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Pushed to GitHub successfully!" -ForegroundColor Green
} else {
    Write-Host "  ✗ Push failed. Check your git credentials or network." -ForegroundColor Red
    Write-Host "  Try running: git push origin master" -ForegroundColor Cyan
}
Write-Host ""

# Step 5: Restore stashed changes (if any)
Write-Host "Step 5: Checking for stashed changes..." -ForegroundColor Green
$stashList = git stash list
if ($stashList) {
    Write-Host "  Found stashed changes. Restoring..." -ForegroundColor Yellow
    git stash pop
    Write-Host "  ✓ Stashed changes restored" -ForegroundColor Green
} else {
    Write-Host "  ℹ No stashed changes" -ForegroundColor Gray
}
Write-Host ""

# Final status
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "📊 Current Git Status:" -ForegroundColor Yellow
Write-Host "=" * 70 -ForegroundColor Cyan
git status
Write-Host ""

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "✅ DONE! Next Steps:" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "1. Go to your Streamlit Cloud dashboard" -ForegroundColor Cyan
Write-Host "2. Wait 2-3 minutes for auto-redeploy" -ForegroundColor Cyan
Write-Host "3. Or click 'Reboot app' to manually trigger deployment" -ForegroundColor Cyan
Write-Host "4. Check the deployment logs for any errors" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔗 Streamlit Cloud: https://share.streamlit.io/" -ForegroundColor Yellow
Write-Host ""
