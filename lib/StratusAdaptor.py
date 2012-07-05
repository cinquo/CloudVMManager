import checkstatus
import time

class StratusAdaptor:

    def __init__(self):
        pass

    def startvm(self):
        a=checkstatus.runCommand("stratus-run-instance --endpoint=$STRATUSLAB_ENDPOINT --username=$STRATUSLAB_USERNAME --password=$STRATUSLAB_PASSWORD --key=$STRATUSLAB_KEY  $IMG")
        return a

 
    def stopvm(self, vmid):
        checkstatus.runCommand("stratus-kill-instance --endpoint=$STRATUSLAB_ENDPOINT --username=$STRATUSLAB_USERNAME --password=$STRATUSLAB_PASSWORD "+vmid)



    def vmstatus(self,p):
        vm_id=runCommand("stratus-describe-instance|awk "+p)
        return vm_id
    

    def execscript(self, vm_ip,master):
        s="ssh -i $PWD/$STRATUSLAB_PRIVATE_KEY -o StrictHostKeyChecking=no -l root "+vm_ip+" 'wget http://dl.dropbox.com/u/21527180/wnconfig.sh;chmod 755 wnconfig.sh;. ./wnconfig.sh "+master+"'"
        File=open("wnconf.sh",'w')
        File.write(s)
        File.close()


    def configure_vm(self,vm_ip,master):
        a="0"
        while a=="0":
            time.sleep(120)
            a=checkstatus.runCommand("stratus-describe-instance|grep "+vm_ip+"| awk '{print $4}'")
            a=str(a[0][0])
        if a!="0":
            time.sleep(240)
            r=StratusAdaptor()
            StratusAdaptor.execscript(r, vm_ip, master)
            checkstatus.runCommand(". ./wnconf.sh")
