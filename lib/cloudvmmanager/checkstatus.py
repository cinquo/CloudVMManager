import subprocess
import time
import logging
import ConfigParser, os
import os

#LOG_DIR = os.getcwd()
#to get all values from configuration file and write to configLog
def getConfig(config):
    LOG_DIR=os.getcwd()+'/LOGS'
    FILE =open(LOG_DIR+'/configLog','w')
    x=config.get('jobs', 'MAX_JOBS_RUNNING')
    y=config.get('jobs', 'MAX_WORKER_NODES')
    z=config.get('jobs','WN_SHUTDOWN_DELAY')
    FILE.write('\nTIMESTAMP:'+str(time.asctime( time.localtime(time.time()) )))
    FILE.write('\nMAXIMUM NO. OF WORKER NODES: '+str(config.get('jobs', 'MAX_WORKER_NODES')))
    FILE.write('\nMAXIMUM NO. OF JOBS RUNNING: '+str(config.get('jobs', 'MAX_JOBS_RUNNING')))
    FILE.write('\nSLEEP TIME :'+str(config.get('jobs','SLEEPTIME')))
    FILE.write('\nWORKER NODE SHUTDOWN DELAY: '+str(config.get('jobs','WN_SHUTDOWN_DELAY')))
    FILE.close()
    return x, y, z, LOG_DIR

#function for running any command in bash
def runCommand(command):
    pipe = subprocess.Popen(command, stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE, shell = True)
    stdout, stderr = pipe.communicate()
    return stdout, pipe.returncode

#function for running command condor_status
def cstatus(z):
    a=runCommand("condor_status|"+z)
    return a
#function for running command condor_q
def cq(z):
    b=runCommand("condor_q|"+z)
    return b

def main(config, logger):
    x, y, z, LOG_DIR = getConfig(config)
    #to check for exit code of the executed commands
    a=cstatus("grep /LINUX|awk '{print $2}'")
    if a[1]!=0:
        logger.error('condor_status failed with exitcode ' + str(a[2]))
        return False
    b=cq("grep jobs|awk '{print $1}'")
    if b[1]!=0:
        logger.error("condor_q failed with exitcode " + str(b[2]))
        return False
    c=cq("grep completed|awk '{print $3}'")
    if c[1]!=0:
        logger.error("condor_q failed with exitcode " + str(c[2]))
        return False
    d=cq("grep running|awk '{print $9}'")
    if d[1]!=0:
        logger.error("condor_q failed with exitcode " + str(d[2]))
        return False
    e=cq("grep idle|awk '{print $7}'")
    if e[1]!=0:
        logger.error("condor_q failed with exitcode " + str(e[2]))
        return False
    f=cq("grep held|awk '{print $11}'")
    if f[1]!=0:
        logger.error("condor_q failed with exitcode " + str(f[2]))
        return False
    try:
        logger.info('\nTIMESTAMP:'+str(time.asctime( time.localtime(time.time()) ))+'\nNumber of worker nodes : '+a[0]+'\nNumber of jobs submitted :'+b[0]+'\nNumber of jobs completed :'+str(c[0])+'\nNumber of jobs running :'+str(d[0])+'\nNumber of idle jobs :'+str(e[0])+'\nNumber of held jobs :'+str(f[0]))
        if a[0]<b[0]:
            logger.info('\nStart '+str(int(b[0])-int(a[0]))+' more worker node(s)')
        elif a[0]>b[0]:
            #to shutdown nodes that are idle for too long
            q=runCommand( "condor_status -verbose|grep -E 'Machine = |TotalTimeUnclaimedIdle'|awk '{ print $3 }'")
            #print q
            q= q[0].split('\n')
            q.remove('')
            #print q
            t=0
            p=0
            for i in q:
                #print q[p], q[p+1]
                if int(q[p+1])<int(z):
                    t+=1
                if int(q[p+1])>int(z):
                    #print 'Shutting down worker node :'+ q[p]
                    t-=1
                    logger.info('Shutting down worker node :'+ q[p]+' because it is unused for a long time')
                if p+3<len(q)-1:
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