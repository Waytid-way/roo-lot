# Force Add Model File to Git
# This script will forcefully add the model file even if ignored

Set-Location "C:\Users\com\Documents\AIE322\RooLord\roo-lot"

Write-Host "=== Checking Model Files ===" -ForegroundColor Cyan

# Check if file exists
$modelFile = "models/electricbills_predict.pkl"
if (Test-Path $modelFile) {
    $size = (Get-Item $modelFile).Length / 1MB
    Write-Host "✓ File exists: $modelFile ($([math]::Round($size, 2)) MB)" -ForegroundColor Green
} else {
    Write-Host "✗ File NOT found: $modelFile" -ForegroundColor Red
    exit 1
}

# Check if file is tracked by git
Write-Host "`n=== Checking Git Status ===" -ForegroundColor Cyan
$tracked = git ls-files $modelFile
if ($tracked) {
    Write-Host "File is already tracked by git" -ForegroundColor Yellow
} else {
    Write-Host "File is NOT tracked by git (needs to be added)" -ForegroundColor Yellow
}

# Check .gitignore rules
Write-Host "`n=== Testing .gitignore Rules ===" -ForegroundColor Cyan
$ignored = git check-ignore -v $modelFile
if ($ignored) {
    Write-Host "File IS ignored by .gitignore:" -ForegroundColor Yellow
    Write-Host "  $ignored" -ForegroundColor Gray
} else {
    Write-Host "File is NOT ignored" -ForegroundColor Green
}

# Force add the file
Write-Host "`n=== Force Adding Model File ===" -ForegroundColor Cyan
git add -f $modelFile
Write-Host "Executed: git add -f $modelFile" -ForegroundColor Gray

# Check staging area
Write-Host "`n=== Checking Staging Area ===" -ForegroundColor Cyan
$staged = git diff --cached --name-only
if ($staged -match "electricbills_predict.pkl") {
    Write-Host "✓ File is now staged for commit!" -ForegroundColor Green
} else {
    Write-Host "✗ File was NOT staged (something is wrong)" -ForegroundColor Red
    Write-Host "`nTrying alternative method..." -ForegroundColor Yellow
    
    # Alternative: temporarily modify .gitignore
    $gitignoreContent = Get-Content .gitignore
    $newContent = $gitignoreContent | Where-Object { $_ -notmatch "^\*.pkl$" -and $_ -notmatch "^!models/electricbills_predict.pkl$" }
    $newContent | Set-Content .gitignore.tmp
    
    # Add file
    Move-Item .gitignore .gitignore.bak -Force
    Move-Item .gitignore.tmp .gitignore -Force
    git add $modelFile
    
    # Restore .gitignore
    Move-Item .gitignore.bak .gitignore -Force
    
    Write-Host "✓ Used alternative method" -ForegroundColor Green
}

# Show what will be committed
Write-Host "`n=== Files Ready to Commit ===" -ForegroundColor Cyan
git diff --cached --name-status

Write-Host "`n=== Next Steps ===" -ForegroundColor Yellow
Write-Host "Run these commands:" -ForegroundColor Cyan
Write-Host '  git commit -m "Add model file for Streamlit deployment"' -ForegroundColor White
Write-Host '  git push origin master' -ForegroundColor White
