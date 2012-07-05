import subprocess

#function for running any command in bash
def runCommand(command):
    pipe = subprocess.Popen(command, stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE, shell = True)
    stdout, stderr = pipe.communicate()
    return stdout, pipe.returncode

