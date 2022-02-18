@echo off
pushd "%~dp0"
if exist .venv\ (
    call ".venv\Scripts\activate.bat"
)
python -m vrcwatch --with-analog --interval 0.1 %*
popd
