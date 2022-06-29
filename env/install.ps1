python -m venv "venv"

./venv/Scripts/Activate.ps1

# install some basic packages
python -m pip install --upgrade pip
python -m pip install --upgrade wheel setuptools pip-tools
# install everything in requirements.txt
./env/sync.ps1

python -m pip install -e .

# install files
pretty-jupyter install-dev