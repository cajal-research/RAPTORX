@echo off
REM Generate the .diff file with commit changes
git diff > commit_changes.diff

REM Append your specific pattern to the end of the .diff file, properly escaping & characters
echo. >> commit_changes.diff
echo Can you please summarize the diff above into the following snippet format?      >> commit_changes.diff
echo ```>> commit_changes.diff
echo commit title >> commit_changes.diff
echo   - commit key point 1 >> commit_changes.diff
echo   - commit key point 2 >> commit_changes.diff
echo   - commit key point 3 >> commit_changes.diff
echo ``` >> commit_changes.diff
echo Please do not use camel case. >> commit_changes.diff
echo Please do not use 'commit title: x', just write 'x' instead >> commit_changes.diff


echo Diff file created and customized in the current directory.
