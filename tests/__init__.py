import os
import subprocess
#from coverage.control import coverage, process_startup

def run(cmd):
    env = os.environ
    #env['COVERAGE_PROCESS_START'] = 'tests/.coveragerc'
    #env['NOSE_WITH_COVERAGE'] = 'true'
    #process_startup()
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, env=env)
    stdout, stderr = proc.communicate()
    return (stdout, stderr, proc.returncode)
