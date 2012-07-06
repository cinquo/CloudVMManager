import subprocess
import time
import logging
import ConfigParser, os
import os
from cloudvmmanager.StratusAdaptor import StratusAdaptor
from cloudvmmanager.utils import runCommand


#to get all values from configuration file and write to configLog

def getConfig(config,logger):
    LOG_DIR='/tmp/my_controller_LOGS'
    x=config.get('jobs', 'MAX_JOBS_RUNNING')
    y=config.get('jobs', 'MAX_WORKER_NODES')
    z=config.get('jobs','WN_SHUTDOWN_DELAY')
    master=config.get('jobs', 'MASTER_IP')
    logger.info('\nTIMESTAMP:'+str(time.asctime( time.localtime(time.time()) )))
    logger.info('\nMASTER:'+str(config.get('jobs','MASTER_IP')))
    logger.info('\nMAXIMUM NO. OF WORKER NODES: '+str(config.get('jobs', 'MAX_WORKER_NODES')))
    logger.info('\nMAXIMUM NO. OF JOBS RUNNING: '+str(config.get('jobs', 'MAX_JOBS_RUNNING')))
    logger.info('\nSLEEP TIME :'+str(config.get('jobs','SLEEPTIME')))
    logger.info('\nWORKER NODE SHUTDOWN DELAY: '+str(config.get('jobs','WN_SHUTDOWN_DELAY')))
    return x, y, z, LOG_DIR,master

#function for running command condor_status
def cstatus(z):
    a=runCommand("condor_status|"+z)
    return a
#function for running command condor_q
def cq(z):
    b=runCommand("condor_q|"+z)
    return b

def main(config, logger):
    x, y, z, LOG_DIR,master = getConfig(config,logger)
    #to check for exit code of the executed commands
    a=cstatus("grep /LINUX|awk '{print $2}'")
    if a[1]!=0:
        logger.error('condor_status failed with exitcode ' + str(a[2]))
        return False
    b=cq("grep jobs|awk '{print $1}'")
    if b[1]!=0:
        logger.error("condor_q failed with exitcode " + str(b[2]))
        return False
    d=cq("grep running|awk '{print $5}'")
    if d[1]!=0:
        logger.error("condor_q failed with exitcode " + str(d[2]))
        return False
    e=cq("grep idle|awk '{print $3}'")
    if e[1]!=0:
        logger.error("condor_q failed with exitcode " + str(e[2]))
        return False
    f=cq("grep held|awk '{print $7}'")
    if f[1]!=0:
        logger.error("condor_q failed with exitcode " + str(f[2]))
        return False
    try:
        logger.info('\nTIMESTAMP:'+str(time.asctime( time.localtime(time.time()) ))+'\nNumber of worker nodes : '+a[0]+'\nNumber of jobs submitted :'+b[0]+'\nNumber of jobs running :'+str(d[0])+'\nNumber of idle jobs :'+str(e[0])+'\nNumber of held jobs :'+str(f[0]))
        s=StratusAdaptor()
        t=0
        if a[0]=='' or a[0]="":
            a[0]=0
        if a[0]<b[0] and int(a[0])<=int(y):
            if int(b[0])<=int(y):
                more_wn=int(b[0])-int(a[0])
            else:
                more_wn=int(y)-int(a[0])
            logger.info('\nStart '+str(more_wn)+' more worker node(s)')
            new_list=[]
            for i in range(0,more_wn):
                new=StratusAdaptor.startvm(s)
                new=new[0][new[0].index('134.'):new[0].index('Done')-5]
                new_list.append(new)
            for i in new_list:
                st=StratusAdaptor.configure_vm(s,i,master)
                if st!=0:
                    logger.warning("Machine failed to start....Killing instance "+st)
        elif a[0]>b[0]:
            #to shutdown nodes that are idle for too long
            q=runCommand( "condor_status -verbose|grep -E 'Machine = |EnteredCurrentActivity|Activity'|grep -v 'ClientMachine ='|awk '{ print $3 }'")
            q= q[0].split('\n')
            q.remove('')
            p=0
            for i in q:
                if int(time.time())-int(q[p+2])<int(z) and q[p+1]=='"Idle"':
                    t+=1
                if int(time.time())-int(q[p+2])>int(z) and q[p+1]=='"Idle"':
                    print 'Shutting down worker node :'+ q[p]
                    t-=1
                    mip=q[p][q[p].index('-')+1:q[p].index('.')]
                    vm_id=StratusAdaptor.vmstatus(s,'{print $1}')
                    vm_ip=StratusAdaptor.vmstatus(s,'{print $6}')
                    vm_id=vm_id[0].split('\n')
                    vm_id=vm_id[1:]
                    vm_id.remove('')
                    print vm_id
                    vm_ip=vm_ip[0].split('\n')
                    vm_ip.remove('')
                    vm_ip.remove('ip')
                    print vm_ip
                    maddr='134.158.75.'+mip
                    logger.info('Shutting down worker node :'+ q[p]+':'+maddr+' because it is unused for a long time')
                    for i in vm_ip:
                        if i==maddr:
                            g=vm_ip.index(i)
                    StratusAdaptor.killvm(s,vm_id[g])
                if p+3<len(q):
                    p+=3
                else:
                    break
        #to check if there are idle jobs and also idle machines
        if int(e[0])>0 and t>0:
            logger.warning('\nJobs idle...not yet assigned to idle machines') 

        #to check if there are too many jobs
        if int(x)<int(d[0]):
            logger.error('\nToo many jobs running..Please remove some jobs')
        #to check if there are no more worker nodes
        if int(y)<int(a[0]):
            logger.error('\nMaximum worker nodes limit is reached. Cannot start any more worker nodes!!')
    except IOError, ioer:
        print ioerr
        logger.error('\nI/O Error occurred')
        return False

    return True

if __name__=="__main__":
    config = ConfigParser.ConfigParser()
    config.readfp(open('jobconfig.cfg'))
    main(config, logger)                     

