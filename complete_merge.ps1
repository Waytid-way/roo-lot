# Complete Git Merge Script
Set-Location "C:\Users\com\Documents\AIE322\RooLord\roo-lot"

# Kill any vim processes
Get-Process | Where-Object {$_.ProcessName -match "vim|vi"} | Stop-Process -Force -ErrorAction SilentlyContinue

# Set git editor to something simple
$env:GIT_EDITOR = "notepad"

# Check if we're in a merge state
if (Test-Path ".git/MERGE_HEAD") {
    Write-Host "Completing merge..."
    git commit --no-edit --allow-empty 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Merge completed successfully!"
        
        # Now push
        Write-Host "Pushing to remote..."
        git push origin master
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Push successful!"
        } else {
            Write-Host "Push failed. You may need to pull again."
        }
    } else {
        Write-Host "Merge commit failed. Trying alternative method..."
        git merge --continue
    }
} else {
    Write-Host "No merge in progress. Checking status..."
    git status
}

# Restore stashed changes if any
$stashList = git stash list
if ($stashList) {
    Write-Host "Restoring stashed changes..."
    git stash pop
}
