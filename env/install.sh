python -m venv "venv"

source venv/bin/activate

# install some basic packages
python -m pip install --upgrade pip
python -m pip install --upgrade wheel setuptools pip-tools
# install everything in requirements.txt
sh env/sync.sh