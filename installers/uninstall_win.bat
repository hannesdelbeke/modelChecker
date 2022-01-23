:: Check for Python Installation
cls
@echo off
echo Checking for Pyhton is in your system...
timeout /t 1 /nobreak>nul
for /f "delims=" %%i in ('python --version 2') do set output=%%i

echo %output% is the Python current version installed in your system 

if errorlevel 1 goto errorNoPython

:: Reaching here means Python is installed.
:: Execute stuff...
echo.
echo modelChecker uninstalling...
echo.
timeout /t 1 /nobreak>nul
python uninstaller.py

:: Once done, exit the batch file -- skips executing the errorNoPython section
goto:eof

:errorNoPython
echo.
echo Error^: Python not installed. You need to have Pyhton installed to run the script.