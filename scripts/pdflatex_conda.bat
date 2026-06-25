@echo off
REM Wrapper to activate Conda env and run pdflatex (with debug)
call "C:\Users\story\miniconda3\Scripts\activate.bat" "C:\Users\story\miniconda3\envs\paper"
where pygmentize || echo "pygmentize not found"
where python || echo "python not found"
echo PATH=%PATH%
"C:\texlive\2025\bin\windows\pdflatex.exe" %*
EXIT /B %ERRORLEVEL%
