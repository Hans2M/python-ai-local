@echo off
cd /d "%~dp0"
python cliente.py temas
echo.
python cliente.py estado
echo.
pause
