@echo off
echo Cleaning up temporary repository clones...
cd /d "%~dp0"

if exist "temp_repos" (
    echo Removing temp_repos directory...
    rmdir /s /q temp_repos
    echo Creating fresh temp_repos directory...
    mkdir temp_repos
    echo Done! Temporary repositories cleaned up.
) else (
    echo temp_repos directory doesn't exist. Creating it...
    mkdir temp_repos
    echo Done!
)

pause