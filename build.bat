@echo off
REM Build CheatBot.exe (Windows). Richiede Python e PyInstaller.
REM Esegui dalla cartella CheatBot: build.bat

pip install -r requirements.txt
pip install pyinstaller

pyinstaller --onefile --noconsole --name CheatBot main.py

echo.
echo Build completata. Trovi CheatBot.exe in: dist\
echo Copia config.txt (da config.txt.example) nella stessa cartella di CheatBot.exe.
if not exist "dist\config.txt" copy config.txt.example dist\config.txt
echo.
pause
