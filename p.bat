@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "PY=%SCRIPT_DIR%p.py"

if "%~1"=="" (
    python "%PY%" -help
    goto :eof
)

REM Help and list are simple pass-throughs
if /I "%~1"=="help" goto run_py
if /I "%~1"=="-help" goto run_py
if /I "%~1"=="--help" goto run_py
if /I "%~1"=="/?" goto run_py
if /I "%~1"=="-list" goto run_py

REM -cd must be handled in BAT so the working directory actually changes in cmd.exe
if not "%~2"=="" (
    if /I "%~2"=="-cd" goto cd_mode
)

:run_py
python "%PY%" %*
goto :eof


:cd_mode
set "ALIAS=%~1"
set "TARGET_PATH="

for /f "usebackq delims=" %%P in (`python "%PY%" "%ALIAS%" --print-path`) do (
    set "TARGET_PATH=%%P"
)

if not defined TARGET_PATH (
    echo Alias "%ALIAS%" not found.
    goto :eof
)

if not exist "%TARGET_PATH%" (
    echo Path does not exist: "%TARGET_PATH%"
    goto :eof
)

cd /d "%TARGET_PATH%"
goto :eof
