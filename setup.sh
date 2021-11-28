#!/bin/bash
echo "Installing correct version of Python and pip"
sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip

echo "Now installing all necessary python modules. Likely most will already be installed."
#confirm all necessary modules are installed
pip3 install argparse
pip3 install subprocess
pip3 install os
pip3 install datetime
pip3 install json
pip3 install hashlib
