@echo off

echo Starting GPAC...
cd C:/Users/meij1/Videos/OdoCSV/GPAutoConnect/

"C:\Dell\Miniconda3\envs\py3.9\python.exe" get_screen_size.py
"C:\Dell\Miniconda3\envs\py3.9\python.exe" GPAC.py

if ERRORLEVEL == 0 echo GPAC Completed

pause && exit

