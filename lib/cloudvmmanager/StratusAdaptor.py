from cloudvmmanager.utils import runCommand
import time

class StratusAdaptor:

    def __init__(self):
        pass

    def startvm(self):
        a=runCommand("stratus-run-instance --endpoint=$STRATUSLAB_ENDPOINT --username=$STRATUSLAB_USERNAME --password=$STRATUSLAB_PASSWORD --key=$STRATUSLAB_KEY  $IMG")
        return a

 
    def stopvm(self, vmid):
        runCommand("stratus-kill-instance --endpoint=$STRATUSLAB_ENDPOINT --username=$STRATUSLAB_USERNAME --password=$STRATUSLAB_PASSWORD "+vmid)



    def vmstatus(self,p):
        vm_id=runCommand("stratus-describe-instance|awk "+p)
        return vm_id
    

    def execscript(self, vm_ip,master):
        s="ssh -i $PWD/stratuslab-client/stratuslab/.ssh/_id_rsa -o StrictHostKeyChecking=no -l root "+vm_ip+" 'wget http://dl.dropbox.com/u/21527180/wnconfig.sh;chmod 755 wnconfig.sh;. ./wnconfig.sh "+master+"'"
        File=open("wnconf.sh",'w')
        File.write(s)
        File.close()


    def configure_vm(self,vm_ip,master):
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
        if a!="0" and b!="Failed":
            time.sleep(240)
            StratusAdaptor.execscript(r, vm_ip, master)
            runCommand(". ./wnconf.sh")
            return 0
        elif b=="Failed":
            vmid=runCommand("stratus-describe-instance|grep "+vm_ip+"| awk '{print $1}'")
            vmid=str(vmid[0][:-1])
            StratusAdaptor.stopvm(r,vmid)
            return vmid
