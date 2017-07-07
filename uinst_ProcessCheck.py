import fileinput
import time
import os
from sys import stdout
from wac_functions import FindProcess
import test_file as tf

proc_list = ['Wacom_Tablet.exe', 'Wacom_TabletUser.exe', 'Wacom_TouchUser.exe', 'WTabletServicePro.exe', 'WacomHost.exe']
_dn, _fn, _lt = tf.MetaLoad()
t_file = tf.LoadFile(_dn, _fn)

# Hard-code wait for system to boot
for i in reversed(range(60)):
    stdout.write("\rCommence file check in %d seconds" % i)
    stdout.flush()
    time.sleep(1)


# Code block that searches process list for the Wacom driver processes to ensure they are running
_name = 'finst_ProcessCheck'
pcount = 1
pc_map = {}
_result = True
for name in proc_list:
    wProc, wPID, wStatus = FindProcess(name)

    if not wProc:
        _result = False
        _e = 'FailedProcess %i' % pcount
        pc_map[_e] = name
        pcount += 1
t_file = tf.AddTest(t_file, _name, _result, pc_map)

# Code block that checks file paths for files installed by driver
_name = 'finst_FileCheck'
fcount = 1
fc_map = {}
_result = True
for line in fileinput.input("C:/Wacomation/resources/driver_files.txt"):
    check = os.path.exists(line.strip())
    if not check:
        _result = False
        _e = 'MissingFile %i' % fcount
        fc_map[_e] = line
        fcount += 1
t_file = tf.AddTest(t_file, _name, _result, fc_map)
