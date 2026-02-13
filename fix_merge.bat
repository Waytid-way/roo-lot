@echo off
REM Fix Git Merge Script for Windows
cd /d C:\Users\com\Documents\AIE322\RooLord\roo-lot

echo Killing vim processes...
taskkill /F /IM vim.exe 2>NUL
taskkill /F /IM vi.exe 2>NUL
taskkill /F /IM gvim.exe 2>NUL

echo Setting git editor...
git config core.editor "echo"

echo Completing merge...
git commit --no-edit

if %ERRORLEVEL% EQU 0 (
    echo Merge completed!
    echo Pushing to remote...
    git push origin master
    
    if %ERRORLEVEL% EQU 0 (
        echo Push successful!
        echo Restoring stashed changes...
        git stash pop
        echo.
        echo === DONE! ===
        git status
    ) else (
        echo Push failed!
    )
) else (
    echo Commit failed!
)

pause
