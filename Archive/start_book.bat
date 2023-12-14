:: Author: jaboll
@echo off
setlocal enabledelayedexpansion


FOR /F "tokens=2*" %%A IN ('REG.EXE Query "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.pdf\UserChoice" /V ProgID') DO (

	FOR /F "tokens=2*" %%C IN ('REG.EXE Query "HKEY_CLASSES_ROOT\%%~B\shell\open\command"') DO (

        FOR /F "delims=-" %%E IN (%%D) DO (
            echo %%E
            set pdfopener="%%E
        )
    )

)

for %%i in ("%CD%\*_BOOK.pdf") do (
    start !pdfopener! %%i
)
