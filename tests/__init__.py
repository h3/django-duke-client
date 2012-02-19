import os
import subprocess
import coverage

def run_duke(cmd):
    coverage.process_startup()
    env = os.environ
    env['COVERAGE_PROCESS_START'] = 'tests/.coveragerc'
    env['NOSE_WITH_COVERAGE'] = 'true'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, env=env)
    stdout, stderr = proc.communicate()
    return (stdout, stderr, proc.returncode)
