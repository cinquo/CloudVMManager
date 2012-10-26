from cloudvmmanager.utils import runCommand
import time
import base64

class StratusAdaptor:

    def __init__(self):
        pass

    def startvm(self, master):
        runCommand("wget --directory-prefix=/tmp/ https://raw.github.com/fbarreir/CloudVMManager/master/wnconfig_analysis.sh --no-check-certificate")
        f = open("/tmp/wnconfig_analysis.sh",'r')
        s = f.read()
        f.close()
        runCommand("rm -f /tmp/wnconfig_analysis.sh")
        a=runCommand('stratus-run-instance --context="EC2_USER_DATA=' + base64.standard_b64encode(s.replace('$1', master, 1)) + '" --endpoint=$STRATUSLAB_ENDPOINT --username=$STRATUSLAB_USERNAME --password=$STRATUSLAB_PASSWORD --key=$STRATUSLAB_KEY  $IMG')
        return a

 
    def stopvm(self, vmid):
        runCommand("stratus-kill-instance --endpoint=$STRATUSLAB_ENDPOINT --username=$STRATUSLAB_USERNAME --password=$STRATUSLAB_PASSWORD "+vmid)



    def vmstatus(self,p):
        vm_id=runCommand("stratus-describe-instance|awk "+p)
        return vm_id
    

    #def execscript(self, vm_ip,master):
        #s="ssh -i $STRATUSLAB_PRIVATE_KEY -o StrictHostKeyChecking=no -l root "+vm_ip+" 'wget http://dl.dropbox.com/u/21527180/wnconfig_analysis.sh;chmod 755 wnconfig_analysis.sh;. ./wnconfig_analysis.sh "+master+"'"
        #File=open("wnconf.sh",'w')
        #File.write(s)
        #File.close()


    def configure_vm(self,vm_ip):
        a="0"
        r=StratusAdaptor()
        while a=="0":
            time.sleep(60)
            a=runCommand("stratus-describe-instance|grep "+vm_ip+"| awk '{print $4}'")
            b=runCommand("stratus-describe-instance|grep "+vm_ip+"| awk '{print $2}'")
            a=str(a[0][0])
            b=str(b[0][:-1])
            if b=="Failed":
                break
        #if a!="0" and b!="Failed":
            #time.sleep(240)
            #StratusAdaptor.execscript(r, vm_ip, master)
            ##optional command for analysis jobs proxy server
            #runCommand("scp -o StrictHostKeyChecking=no -i $STRATUSLAB_PRIVATE_KEY /home/cms001/crab/CMSSW_5_0_1/src/x509up_u15305 root@"+ vm_ip +":/data")
            #runCommand(". ./wnconf.sh")
            #return 0
        if b=="Failed":
            vmid=runCommand("stratus-describe-instance|grep "+vm_ip+"| awk '{print $1}'")
            vmid=str(vmid[0][:-1])
            StratusAdaptor.stopvm(r,vmid)
            return vmid
        return 0
