
if exist "venv\" (
    call venv/Scripts/activate.bat
    python -m game
) else (
    python -m venv venv
    call venv/Scripts/activate.bat
    python -m pip install -r requirements.txt
    python -m game
)