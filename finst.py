from platform import system, release
import subprocess
import glob
import time
import datetime
from sys import stdout
import os
import sys
from wac_functions import *
import test_file as tf
import json

timerStartTime = time.time()  # -- Timer for elapsed install time

testStartTime = datetime.datetime.now()
_date = testStartTime.strftime("%m-%d-%y")
_time = testStartTime.strftime("%H:%M")
_os = system() + " " + release()
test_dir_name = ""
test_file_name = None
test_name = 'finst'
_driver = None
_result = None
_e = None
_error = {}

# Registry Check Code
_fp = open(r'C:\Wacomation\resources\RegList.json', 'r')
_reg = json.load(_fp)
rkeylist = list(_reg.keys())
rkeylist.sort()
for key in rkeylist:
    _key = _reg[key]['Key']
    _subkey = _reg[key]['SubKey']
    s = RegistryKey(_key, _subkey)
    if s:
        vkeydict = _reg[key]['ContainsValues']
        reg_rslt_dict = RegistryValue(vkeydict)
# Code ends here


for driver in glob.glob(r"C:\Wacomation\driver\WacomTablet*.exe"):
    name = os.path.splitext(driver)[0]                           # -- removes .exe from driver name
    test_dir_name = name[33:]                                          # -- removes "WacomTablet_" from driver name
    test_file_name = test_dir_name + " " + _os
    if not os.path.isdir(r"C:\Wacomation\output\%s" % test_dir_name):  #| This block creates a directory hierarchy in the
        os.mkdir(r"C:\Wacomation\output\%s" % test_dir_name)           #| output folder with root directory [dri.ver.num-ber]
    # os.mkdir(r"C:\Wacomation\output\%s\%s" % (dir_name, time))    #| and subdirectories [date-time-stamp of.test]
    _result, _e = InstallDriver(driver)
    if _e is not None:
        _error['InstallFailure'] = _e
   # process = subprocess.Popen([driver, "/s"])

_json = tf.NewFile(test_dir_name, _os, _date, _time)
_report = tf.AddTest(_json, test_name, _result, _error)
tf.SaveFile(test_dir_name, test_file_name, _report)
tf.MetaDump(test_dir_name, test_file_name, test_name)

script = 'finst_ProcessCheck.py'                              #| for next script then restarts
RegEntry(script)
RebootSystem()
