import checkstatus
import time
import ConfigParser, os
import logging
import sys

MAX_CONS_FAILURES = 5

def loadConfig(fileconfigname):
    config = ConfigParser.ConfigParser()
    config.readfp(open(fileconfigname))
    return config

runconfig = loadConfig(os.getcwd()+'/'+sys.argv[1])
a = float(runconfig.get('jobs','SLEEPTIME', 120))
LOG_DIR=str('/tmp/my_controller_LOGS')

logger = logging.getLogger('StatusLog')
hdlr=logging.FileHandler(LOG_DIR+'/StatusLog')
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)



failcounter = 0
while True:
    result = checkstatus.main(runconfig, logger)
    if result is False:
        failcounter += 1
        logger.error('trying to execute command again')
    elif failcounter > 0:
        failcounter = 0
    if failcounter > MAX_CONS_FAILURES:
        print "Error: reached maximum limit of consecutive failures " + str(MAX_CONS_FAILURES)

    time.sleep(a)
