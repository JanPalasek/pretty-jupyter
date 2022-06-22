python -m venv "venv"

source venv/bin/activate

# install some basic packages
python -m pip install --upgrade pip
python -m pip install --upgrade wheel setuptools pip-tools
# install everything in requirements.txt
./env/sync.sh

# install the app
pretty-jupyter install