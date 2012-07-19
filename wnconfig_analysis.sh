#!/bin/sh

conary update condor:runtime;
export PATH=$PATH:/opt/condor/sbin/:/opt/condor/bin/condor/:/etc/condor/:/opt/condor/bin/;
wget http://dl.dropbox.com/u/21527180/condor_config;
#/etc/init.d/condor start;
sed -i 's/HOSTNAME/MHOSTNAME/g' condor_config ;
sed -i '12iMHOSTNAME='$1 condor_config
rm -rf /etc/condor/condor_config;
mv condor_config /etc/condor/;
#condor_reconfig;
sed -i '83icondor       ALL=(ALL)       ALL' /etc/sudoers;
sed -i '12iMHOSTNAME='$1 /etc/init.d/condor;
sed -i 's/CONFIG_CONDOR_UID_DOMAIN:=`hostname -d`/CONFIG_CONDOR_UID_DOMAIN:=$MHOSTNAME/g' /etc/init.d/condor;
sed -i 's/CONFIG_CONDOR_FILESYSTEM_DOMAIN=${CONFIG_CONDOR_FILESYSTEM_DOMAIN:=`hostname -f`/CONFIG_CONDOR_FILESYSTEM_DOMAIN=${CONFIG_CONDOR_FILESYSTEM_DOMAIN:=$MHOSTNAME/g' /etc/init.d/condor;
sed -i 's/CONFIG_CONDOR_MASTER=`hostname -f`/CONFIG_CONDOR_MASTER=$MHOSTNAME/g' /etc/init.d/condor;
#condor_reconfig;
#/etc/init.d/condor stop;

sed -i 's%JAVA = /usr/bin/java%JAVA = /usr/lib/jvm/java-1.6.0-openjdk-1.6.0.0.x86_64/bin/java%' /etc/condor/condor_config


#to configure cvfms
mkdir /data/T1_FR_CCIN2P3

/etc/cernvm/config -c site CERNVM_ORGANISATION=CMS;
/etc/init.d/cvmfs stop;
cp -r /cvmfs/cms.cern.ch/SITECONF/T1_FR_CCIN2P3/* /data/T1_FR_CCIN2P3/;
echo 'export CMS_LOCAL_SITE=/data/T1_FR_CCIN2P3' > /etc/cvmfs/domain.d/cern.ch.local;
/etc/init.d/cvmfs flush;
/etc/init.d/cvmfs restartclean;
wget http://dl.dropbox.com/u/21527180/storage.xml;
wget http://dl.dropbox.com/u/21527180/site-local-config.xml;
mv -f storage.xml /data/T1_FR_CCIN2P3/PhEDEx/;
mv -f site-local-config.xml /data/T1_FR_CCIN2P3/JobConfig/;
chmod -R 777 /home/condor/*;
cd /data;
wget http://dl.dropbox.com/u/21527180/ca.tar.gz;
tar -xvzf ca.tar.gz;
chown -R condor:condor /data/*;
/etc/init.d/cvmfs restartclean;
/etc/init.d/condor start;