from sys import stdout
import subprocess
import time
import test_file as tf
from wac_functions import RebootSystem, RegEntry

_dn, _fn, _lt = tf.MetaLoad()
t_file = tf.LoadFile(_dn, _fn)
_name = 'uinst'
# Hard-code wait for system to fully boot
for i in reversed(range(10)):
    stdout.write("\rUninstalling in %d seconds" % i)
    stdout.flush()
    time.sleep(1)

path = r"C:\Program Files\Tablet\Wacom\32\Remove.exe"

start = time.time()
# Uninstall the driver
process = subprocess.Popen([path, "/u", "/s"], shell=True, cwd=r"C:\Program Files\Tablet\Wacom\32")

# while process is running, show time elapsed during uninstall
while process.poll() is None:
    elapsed = time.time() - start
    stdout.write("\rUinsting. Elapsed time: %d seconds" % elapsed)
    stdout.flush()

_report = {}
_result = True
if process.returncode != 0:          # If call return is 0 (no errors) makes new reg entry for next script then restarts
    _result = False
    _e = 'UninstallFailure'
    rc = process.returncode
    _report[_e] = rc
t_file = tf.AddTest(t_file, _name, _result, _report)

script = 'uinst_ProcessCheck.py'
RegEntry(script)
RebootSystem()
