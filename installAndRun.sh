#!/bin/bash


git clone -b p4 --depth 1 --single-branch  https://gitlab.lrz.de/hpcsoftware/Peano.git ./Peano

cd Peano
libtoolize
aclocal
autoconf
autoheader
cp src/config.h.in .
automake --add-missing
./configure --prefix=$PWD/local --enable-loadbalancing-toolbox --enable-exahype --with-multithreading=cpp
make -j4


# This creates gluecode, compiles and links the peano4 application
#
# NOTE: increasng the argument to --h will make the problem simpler and therefore
# reduce the runtime. Similarly, smaller values supplied to --h increase the complexity
# and hence run time

export PYTHONPATH=$PWD/python:$PYTHONPATH
cd examples/exahype2/euler
wget https://raw.githubusercontent.com/iamholger/euler/master/euler_simple.py
python3 euler_simple.py --h=0.005 --load-balancing-quality=0.9

echo "Done. To run do: $PWD/peano4"
