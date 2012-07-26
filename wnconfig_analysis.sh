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

#sed -i 's%SLOT1_USER.*% %' /etc/condor/condor_config.local
#sed -i 's%ALLOW_WRITE.*%ALLOW_WRITE = *%' /etc/condor/condor_config.local
#sed -i 's%DEDICATED_EXECUTE_ACCOUNT_REGEXP.*%DEDICATED_EXECUTE_ACCOUNT_REGEXP = cms00[1-8]+%' /etc/condor/condor_config.local
sed -i 's%CONDOR_LOCALCONFIG=.*%CONDOR_LOCALCONFIG=/etc/condor/condor_config.local.cernvm%'  /etc/init.d/condor
sed -i '/SLOT1_USER.*/ d' /etc/condor/condor_config.local
sed -i '/ALLOW_WRITE.*/ d' /etc/condor/condor_config.local
sed -i '/DEDICATED_EXECUTE_ACCOUNT_REGEXP.*/ d' /etc/condor/condor_config.local
sed -i '/DAEMON_LIST.*/ d' /etc/condor/condor_config.local
echo 'ALLOW_WRITE = *' >> /etc/condor/condor_config.local
echo 'DEDICATED_EXECUTE_ACCOUNT_REGEXP = cms00[1-8]+' >> /etc/condor/condor_config.local
echo 'DAEMON_LIST = MASTER, STARTD' >> /etc/condor/condor_config.local
export cpus=`cat /proc/cpuinfo | grep processor | wc -l`
for i in $(seq 1 $cpus)
do 
    useradd "cms00$i"
    echo "SLOT"$i"_USER = cms00$i" >> /etc/condor/condor_config.local
done


#to configure cvfms
mkdir /data/T1_FR_CCIN2P3

/etc/cernvm/config -c site CERNVM_ORGANISATION=CMS;
/etc/init.d/cvmfs restartclean;
#cp -r /cvmfs/cms.cern.ch/SITECONF/T1_FR_CCIN2P3/* /data/T1_FR_CCIN2P3/;
echo 'export CMS_LOCAL_SITE=/data/T1_FR_CCIN2P3' > /etc/cvmfs/domain.d/cern.ch.local;
/etc/init.d/cvmfs restartclean;

mkdir /data/T1_FR_CCIN2P3/CVS
mkdir /data/T1_FR_CCIN2P3/phedex

#wget http://dl.dropbox.com/u/21527180/storage.xml;
mkdir /data/T1_FR_CCIN2P3/PhEDEx/
#mv -f storage.xml /data/T1_FR_CCIN2P3/PhEDEx/;
cat <<EOF>/data/T1_FR_CCIN2P3/PhEDEx/storage.xml
<storage-mapping>

<!-- Specific for LoadTest07 export sample -->
  <lfn-to-pfn protocol="direct" path-match=".*/LoadTest07_IN2P3_(.*)_.*_.*"
   result="/pnfs/in2p3.fr/data/cms/export/LoadTest/store/phedex_monarctest/monarctest_IN2P3-DISK1/LoadTest07_IN2P3_$1"/>

  <lfn-to-pfn protocol="srmv2" path-match="/+.*/LoadTest07_Debug_(.*)/IN2P3/(.*)" 
   result="srm://ccsrm.in2p3.fr:8443/srm/managerv2?SFN=/pnfs/in2p3.fr/data/cms/data/store/PhEDEx_LoadTest07/LoadTest07_Debug_$1/IN2P3/$2"/>
  <lfn-to-pfn protocol="srmv2" path-match="/+.*/LoadTest07_Debug_(.*)/FR_CCIN2P3/(.*)" 
   result="srm://ccsrm.in2p3.fr:8443/srm/managerv2?SFN=/pnfs/in2p3.fr/data/cms/data/store/PhEDEx_LoadTest07/LoadTest07_Debug_$1/FR_CCIN2P3/$2"/> 


<!-- Specific for SAM tests -->

  <lfn-to-pfn protocol="srmv2" path-match="/store/unmerged/SAM/(.*)"
    result="srm://ccsrm.in2p3.fr:8443/srm/managerv2?SFN=/pnfs/in2p3.fr/data/cms/prod/store/unmerged/SAM/$1"/>

<!-- production stage out : unmerged -->
  <lfn-to-pfn protocol="direct" path-match="/+(store/unmerged/.*)"
    result="/pnfs/in2p3.fr/data/cms/prod/$1"/>
  <pfn-to-lfn protocol="direct" path-match="/pnfs/in2p3.fr/data/cms/prod/+(store/unmerged/.*)"
    result="/$1"/>

<!-- jobs access protocol - default -->
  <lfn-to-pfn protocol="jobs" chain="dcap" path-match="(.*)"
    result="$1" />
  <pfn-to-lfn protocol="jobs" chain="dcap" path-match="(.*)"
    result="$1" />

<!-- default - production and Protocol chains -->
  <lfn-to-pfn protocol="direct" path-match="/+(.*)"
    result="/pnfs/in2p3.fr/data/cms/data/$1"/>
  <lfn-to-pfn protocol="srm" chain="direct" path-match="/+(.*)"
    result="srm://ccsrm.in2p3.fr:8443/srm/managerv1?SFN=/$1" />

  <lfn-to-pfn protocol="srmv2" chain="direct" destination-match=".*" is-custodial="y"
    path-match="/+(.*)"
    result="srm://ccsrm.in2p3.fr:8443/srm/managerv2?SFN=/$1" space-token="CMSCUSTODIAL"/>

  <lfn-to-pfn protocol="srmv2" chain="direct" destination-match=".*" is-custodial="n"
    path-match="/+(.*)"
    result="srm://ccsrm.in2p3.fr:8443/srm/managerv2?SFN=/$1" space-token="CMS_DEFAULT"/>

  <lfn-to-pfn protocol="dcap" chain="direct" path-match="/+(.*)"
    result="dcap://ccdcapcms/$1" />
  <pfn-to-lfn protocol="direct" path-match="/pnfs/in2p3.fr/data/cms/data/+(.*)"
    result="/$1" />
  <pfn-to-lfn protocol="srm" chain="direct" path-match=".*\?SFN=(.*)"
    result="$1" />
  <pfn-to-lfn protocol="srmv2" chain="direct" path-match=".*\?SFN=(.*)"
    result="$1" />
  <pfn-to-lfn protocol="dcap" chain="direct" path-match="dcap://ccdcapcms(.*)"
    result="$1" />
<lfn-to-pfn protocol="root"
      path-match="/+store/(.*)" result="root://xrootd.ba.infn.it//store/$1"/>
 <pfn-to-lfn protocol="root"
      path-match="root://xrootd.ba.infn.it//store/(.*)" result="/store/$1"/>
</storage-mapping>
EOF

#wget http://dl.dropbox.com/u/21527180/site-local-config.xml;
mkdir /data/T1_FR_CCIN2P3/JobConfig/
#mv -f site-local-config.xml /data/T1_FR_CCIN2P3/JobConfig/;
cat <<EOF>/data/T1_FR_CCIN2P3/JobConfig/site-local-config.xml
<site-local-config>
 <site name="T1_FR_CCIN2P3">
    <event-data>
      <catalog url="trivialcatalog_file:/data/T1_FR_CCIN2P3/PhEDEx/storage.xml?protocol=root"/>
    </event-data>
    <local-stage-out>
      <command value="srmv2-lcg"/>
      <catalog url="trivialcatalog_file:/data/T1_FR_CCIN2P3/PhEDEx/storage.xml?protocol=srmv2"/>
      <se-name value="ccsrm.in2p3.fr"/>
    </local-stage-out>
    <fallback-stage-out>
       <command value="srmv2"/>
       <option value="-debug"/>
       <catalog url="trivialcatalog_file:/data/T1_FR_CCIN2P3/PhEDEx/storage.xml?protocol=srmv2"/>
       <se-name value="ccsrm.in2p3.fr"/>
      </fallback-stage-out>
    <calib-data>
      <frontier-connect>
       <load balance="proxies"/>
         <proxy url="http://cclcgcms01.in2p3.fr:3128"/>
         <proxy url="http://cclcgcms02.in2p3.fr:3128"/>
         <server url="http://cmsfrontier.cern.ch:8000/FrontierInt"/>
         <server url="http://cmsfrontier1.cern.ch:8000/FrontierInt"/>
         <server url="http://cmsfrontier2.cern.ch:8000/FrontierInt"/>
         <server url="http://cmsfrontier3.cern.ch:8000/FrontierInt"/>
      </frontier-connect>
    </calib-data>
 </site>
</site-local-config>
EOF

chown -R condor:condor /data/T1_FR_CCIN2P3;
chmod -R 755 /data/T1_FR_CCIN2P3;

cd /data;
wget http://dl.dropbox.com/u/21527180/ca.tar.gz;
tar -xvzf ca.tar.gz;
chown -R condor:condor /data/*;
/etc/init.d/cvmfs restartclean;
/etc/init.d/condor start;
/etc/init.d/condor restart;
chmod -R 777 /home/condor/*;