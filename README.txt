smart rm tools 
version: 0.2

install:
 
git clone https://github.com/ximik-alexey/smart_rm.git 
cd /smart_rm
python setup.py sdist
cd /dist 
sudo  pip install smart_rm-'version'.tar.gz

uninstall:

sudo pip uninstall smart_rm
