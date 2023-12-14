@echo off
setlocal enabledelayedexpansion
set /p "id=Shape: "
for /f "tokens=1-2 delims=/: " %%a in ('echo %time%') do (set timestamp=%%a-%%b)
for /f "tokens=1-3 delims=/. " %%a in ('echo %date%') do (set datestamp=%%a-%%b-%%c)
@REM mpremote connect COM5 cp :test.csv ./!id!-!timestamp!-!datestamp!.csv
mpremote connect COM5 cp -r :./* .
mpremote connect COM5 rm -r :.
