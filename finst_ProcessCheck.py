import os
import fileinput
from sys import stdout
import time
import json
from test_file import *
from wac_functions import FindProcess, RegEntry, RebootSystem


proc_list = ['Wacom_Tablet.exe', 'Wacom_TabletUser.exe',
             'Wacom_TouchUser.exe', 'WTabletServicePro.exe']
# d_name, _file, _lt = tf.MetaLoad()

# t_file = tf.LoadFile(d_name, _file)


for i in reversed(range(90)):                                           #| Timer block to wait for the system
    stdout.write("\rCommence file check in %i seconds" % i)             #| to fully boot
    stdout.flush()
    time.sleep(1)

# _name = 'Finst Process Check'
pcount = 1
pc_map = {}
missing_file_list = []
missing_path_list = []
path_err = 0
file_err = 0
_result = True
fc_map = {}
for name in proc_list:                                                  #| Code block that searches process list for
    wProc, wPID, wStatus = FindProcess(name)
                                #| the Wacom driver processes to ensure they are running
    if not wProc:
        _result = False
        err = 'failedProcess %i' % pcount
        pc_map[err] = name
        pcount += 1
# t_file = tf.AddTest(t_file, _name, _result, pc_map)

# _name = 'Finst File Check'
fcount = 1
# _result = True
with open(r'C:/Wacomation/resources/FileList.json', 'r') as f:
    fc_map = json.load(f)
pkeylist = list(fc_map.keys())
pkeylist.sort()
for p in pkeylist:
    _path = fc_map[p]['Path']
    print '_path: ' + _path
    raw_input('Enter')

    try:
        pcheck = os.path.exists(_path.strip())
    except IOError as e:
        print(e.errno)
        raw_input('Enter')
    print 'pcheck: ', pcheck
    # print 'pcheck %s: ' %p + str(pcheck)
    # raw_input('Enter')
    if not pcheck:
        path_err += 1
        missing_path_list.append(_path)
    else:
        fkeylist = list(fc_map[p]['ContainsFiles'].keys())
        fkeylist.sort()
        for f in fkeylist:
            _file = fc_map[p]['ContainsFiles'][f]['FileName']
            _size = fc_map[p]['ContainsFiles'][f]['ByteSize']
            # print '_file: ' + pc_map[p]['ContainsFiles'][f]['FileName']
            # print '_size: ' + pc_map[p]['ContainsFiles'][f]['ByteSize']
            # raw_input('Enter')
            f_path = _path + '\\' + _file
            fcheck = os.path.exists(f_path)
            print '%s: ' % f_path, fcheck

            if not fcheck:
                file_err += 1
                missing_file_list.append(f_path)
            # print 'f_path: ' + f_path
            # print 'fcheck: ' + str(fcheck)
            # raw_input('Enter')
print 'path_err: ' + str(path_err)
print 'file_err: ' + str(file_err)
count = 0
while count < len(missing_path_list):
    print 'missing path %i: ' % count + missing_path_list[count]
    count += 1
count2 = 0
while count2 < len(missing_file_list):
    print 'missing file %i' % count2 + missing_file_list[count2]
    count2 += 1
raw_input('Enter')
# t_file = tf.AddTest(t_file, _name, _result, fc_map)

# tf.SaveFile(d_name, _file, t_file)
# tf.MetaDump(d_name, _file, _name)

# script = "uinst.py"                                                      #| Start uinst.py on reboot
# RegEntry(script)
# RebootSystem()                                                           #| Restart the computer.



