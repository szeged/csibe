#!/bin/bash

cd $HOME

echo 'export SHELL="/bin/bash"' >> .bashrc

export SHELL="/bin/bash"

python3 --version

git clone https://github.com/szeged/csibe
cd csibe

./csibe.py native -Os -w
./csibe.py gcc-cortex-m0 gcc-cortex-m4 clang-cortex-m0 clang-cortex-m4 -Os -w
./csibe.py native CSiBE-v2.1.1 -Os -w
./csibe.py native servo
