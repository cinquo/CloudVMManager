CloudVMManager
==============

Daemon to start and stop VM depending on number of worker nodes requested/running.


Info
====

-The python files are located in 'lib' directory
-The code to be executed is located in 'bin' directory
-The configuration files are located in etc directory
-The environment variables are exported in envvar.sh


Steps to configure and run
==========================
1)set the environment variables in envvar.sh according to your environment and source the file
2)Change any configuration details if required in the configuration files
3)Run by typing  bash test.sh <configuration file name with relative path>
4)The process will start running in the background
5)Check the log files to see the required information
