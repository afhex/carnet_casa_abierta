@echo off
cd /d "%~dp0"

echo ===================================
echo Instalando dependencias de Backend
echo ===================================
echo.

echo Instalando con pip...
python.exe -m pip install --upgrade pip
python.exe -m pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ===================================
    echo Instalacion completada con exito!
    echo ===================================
    echo.
    echo Ahora puedes ejecutar:
    echo python -m uvicorn main:app --reload
    echo.
) else (
    echo.
    echo ERROR durante la instalacion
    echo.
)

pause
