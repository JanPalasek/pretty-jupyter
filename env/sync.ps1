venv/Scripts/Activate.ps1
# install from 'requirements.txt'
python -m piptools sync
# install the current modules
python -m pip install -e .