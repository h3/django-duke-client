import subprocess

def run_duke(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    return (stdout, stderr, proc.returncode)
