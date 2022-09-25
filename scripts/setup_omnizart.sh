pip3 install --upgrade cython
git clone https://github.com/Music-and-Culture-Technology-Lab/omnizart.git
cd omnizart
pip install -U pip
pip install numpy
pip install .
omnizart download-checkpoints
cd ..
mkdir songs
