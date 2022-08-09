@echo off
echo Adding all files
git add *
echo Creating commit
git commit -m "Automatic Commit"
echo Pushing to repository
git push -f origin main