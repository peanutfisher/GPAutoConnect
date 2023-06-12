@echo off

echo Connecting GP...
cd C:/Users/meij1/Videos/OdoCSV/GPAutoConnect/

"C:/Users/meij1/3D Objects/Anarchy/Miniconda3/envs/py3.9/python.exe" C:/Users/meij1/Videos/OdoCSV/GPAutoConnect/GPAC.py

if ERRORLEVEL == 0 echo GP Connected

pause && exit

