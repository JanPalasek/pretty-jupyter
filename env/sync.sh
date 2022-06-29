# install from 'requirements.txt'
python -m piptools sync
# install the current modules
python -m pip install -e .
# install pretty jupyter files so jupyter nbconvert works
pretty-jupyter install-dev