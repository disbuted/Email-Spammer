@echo off
setlocal enabledelayedexpansion

set "functionFile=functions.json"

if "%~1"=="" (
    echo Please drag and drop the JSON file you want to add onto this script.
    pause
    exit /b 1
)

if not exist "%~1" (
    echo The file you dragged does not exist: %~1
    pause
    exit /b 1
)

if not exist "%functionFile%" (
    echo functions.json file not found in the same directory as this script.
    pause
    exit /b 1
)

set "newData=%~1"

echo Checking functions.json for any trailing commas...
set "commaFixed=0"

for /f "tokens=*" %%A in ('type "%functionFile%" ^| findstr /v "^$"') do set "lastLine=%%A"

if "!lastLine!"=="}," (
    echo Removing trailing comma...
    set "commaFixed=1"
    > "temp_fixed.json" (
        for /f "tokens=*" %%A in ("%functionFile%") do (
            set "line=%%A"
            if "!line!"=="!lastLine!" (
                echo }
            ) else (
                echo !line!
            )
        )
    )
    move /Y "temp_fixed.json" "%functionFile%" >nul
)

if "%commaFixed%"=="1" (
    echo Trailing comma removed.
) else (
    echo No trailing comma found.
)

echo Adding new data from %newData% to functions.json...
(
    echo,
    type "%newData%"
    echo 
) >> "%functionFile%"

cls
echo Data has been successfully added to functions.json!
pause
endlocal
