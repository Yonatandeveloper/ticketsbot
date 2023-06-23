@echo off

echo Loading installation
pip install -r requirements.txt

echo Starting bot...
start run.bat

echo Deleting Installtion file...
del install.bat

exit