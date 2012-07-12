#! /bin/sh
source /cvmfs/cms.cern.ch/slc5_amd64_gcc462/external/python/2.6.4-cms/etc/profile.d/init.sh 
export PATH=$PATH:$PWD/bin/:$PWD/lib/:<stratuslab client bin path>
export PYTHONPATH=$PYTHONPATH:$PWD/lib/:$PWD/bin/:<also the stratusab client python path>
export STRATUSLAB_KEY=<type your key location>
export STRATUSLAB_PRIVATE_KEY=<type your private key location here>
export STRATUSLAB_USERNAME=<type your username here>
export STRATUSLAB_PASSWORD=<type your password here>
export STRATUSLAB_ENDPOINT=<type your cloud endpoint here>
export IMG=<type your image id here>
