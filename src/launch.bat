@echo off

cd /d "%~dp0"

call venv_win\Scripts\activate

cd src

python main.py

pause