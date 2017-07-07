from _winreg import *
from ntsecuritycon import *
from sys import stdout
from test_file import *
import win32security
import win32api
import psutil
import subprocess
import time


global keyObject
keyObject = None


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Opens registry key with specified subkey #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def RegistryKey(rkey, skey):
    spath = skey
    kres = True
    global keyObject
    if rkey == 'HKEY_USERS':
        try:
            keyObject = OpenKey(HKEY_USERS, spath)
        except WindowsError:
            kres = False
    else:
        try:
            keyObject = OpenKey(HKEY_LOCAL_MACHINE, spath)
        except WindowsError:
            kres = False
    return kres



# Checks value info for subkey
# Returns dict of missing values

def RegistryValue(json_report):
    test_name = "Registry Check"
    result = True
    path = r'C:\Wacomation\resources\RegList.json'
    with open(path, 'r') as f:
        val_dict = json.load(f)
    f.close()
    typeList = ['NONE', 'REG_SZ', 'REG_EXPAND_SZ', 'REG_BINARY', 'REG_DWORD',
                                                          'REG_DWORD_BIG_ENDIAN', 'REG_LINK', 'REG_MULTI_SZ',
                                                          'REG_RESOURCE_LIST', 'REG_FULL_RESOURCE_DESCRIPTOR',
                                                          'REG_RESOURCE_REQUIREMENTS_LIST', 'REG_QWORD']
    # The numerical list position of each of the above RegTypes corresponds with the matching "q_type" integer value
    # returned by the _winreg.EnumValue method. These should not change, so maybe convert to tuple

    error_map = {}
    kcount = 1
    vkeylist = list(val_dict.keys())
    vkeylist.sort()
    for val in vkeylist:
        valCompareResult = False
        vname = val_dict[val]['Name']
        vtype = val_dict[val]['Type']
        vdata = val_dict[val]['Data']
        _name = vname.strip()
        _type = vtype
        _data = vdata
        sk, v, lm = QueryInfoKey(keyObject)
        i = 0
        errcout = 0
        while i < v:
            while not valCompareResult:
                q_name, q_data, q_type = EnumValue(keyObject, i)
                _compare = cmp(str(q_data), str(_data.strip('"')))
                q_type = typeList[q_type]
                if _name == '(Default)':
                    _name = ''
                if (_name, _compare, _type) == (q_name, 0, q_type):
                    valCompareResult = True
            i += 1
        errcout += 1
        result = False
        cout = str(errcout)
        error_map[cout]['Name'] = vname
        error_map[cout]['Type'] = vtype
        error_map[cout]['Data'] = vdata
    results_map = AddTest(json_report, test_name, result, error_map)
    return results_map


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Method that assigns the next script to run on startup #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def RegEntry(d, s):
    RegPath = r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"
    RunOnce = OpenKey(HKEY_CURRENT_USER, RegPath, 0, KEY_WRITE)
    SetValueEx(RunOnce, "Test Automation", 0, REG_SZ, r"C:\%s\scripts\%s" % (d, s))
    CloseKey(RunOnce)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Function that adjusts privileges so the script can perform a reboot  #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def AdjustPrivilege(priv, enable=1):
    # Get process token
    flags = TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY
    htoken = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
    # Get the ID for the system shutdown privilege
    id = win32security.LookupPrivilegeValue(None, priv)  # params = (systemName, privilegeName)
    # Obtain the privilege for this process
    # Create a list of privileges to be added
    if enable:
        newPrivileges = [(id, SE_PRIVILEGE_ENABLED)]
    else:
        newPrivileges = [(id, 0)]
    # make the privilege adjustment
    win32security.AdjustTokenPrivileges(htoken, 0, newPrivileges)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Function that adjusts privileges and performs reboot when called  #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def RebootSystem(message="Rebooting", timeout=0, bForce=1, bReboot=1):
    AdjustPrivilege(SE_SHUTDOWN_NAME)
    try:
        win32api.InitiateSystemShutdown(None, message, timeout, bForce, bReboot)
    finally:
        # Remove privilege just added
        AdjustPrivilege(SE_SHUTDOWN_NAME, 0)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Function that iterates through process list to find process "pname,"  #
# then returns true, PID, and status when found                         #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def FindProcess(pname):
    n = False
    pid = 0
    pstat = 'not found'
    for process in psutil.process_iter():
        process = psutil.Process(process.pid)
        proc_name = process.name()
        if proc_name == pname:
            pid = process.pid
            pstat = process.status()
            n = True
    return n, pid, pstat


def ProcessTest(json_report):
    error = {}
    i = 0
    result = True
    test_name = "Process Check"
    proc_list = ['Wacom_Tablet.exe', 'Wacom_TabletUser.exe',
                 'Wacom_TouchUser.exe', 'WTabletServicePro.exe', 'WacomHost.exe']
    for name in proc_list:
        res, pid, pstatus = FindProcess(name)
        if not res:
            result = False
            i += 1
            error[i] = name + " " + pstatus
    results_map = AddTest(json_report, test_name, result, error)
    return results_map


def FileTest(json_report):
    error_map = dict()
    missing_count = 0
    test_name = "File Check"
    result = True
    with open(r'C:\Wacomation\resources\FileList.json', 'r') as f:
        file_map = json.load(f)
    pkeylist = list(file_map.keys())
    pkeylist.sort()
    for p in pkeylist:
        _path = file_map[p]['Path']
        pcheck = os.path.exists(_path)
        if not pcheck:
            missing_count += 1
            result = False
            error_map.update([(missing_count, _path)])
        else:
            fkeylist = list(file_map[p]['ContainsFiles'].keys())
            fkeylist.sort()
            for f in fkeylist:
                _file = file_map[p]['ContainsFiles'][f]['FileName']
                f_path = _path + '\\' + _file
                fcheck = os.path.exists(f_path)
                # _size = file_map[p]['ContainsFiles'][f]['ByteSize']
                if not fcheck:
                    missing_count += 1
                    error_map.update([(missing_count, f_path)])
    results_map = AddTest(json_report, test_name, result, error_map)
    return results_map

def InstallDriver():
    driver = getMetaValue('driverName')
    start = time.time()
    process = subprocess.Popen([driver, "/s"])
    while process.poll() is None:         # Function to show elapsed install C:\Users\Cash\Desktop\setuptools-19.6.1time
        elapsed = time.time() - start
        stdout.write("\rFinsting. Elapsed time: %d" % elapsed)
        stdout.flush()
    _result = True
    _error = None
    if process.returncode != 0:          # If call return is 0 (no errors) makes new reg entry
        _result = False
        _error = process.returncode
    return _result, _error


def UninstallDriver():
    start = time.time()
    path = r"C:\Program Files\Tablet\Wacom\32\Remove.exe"
    process = subprocess.Popen([path, "/u", "/s"], shell=True, cwd=r"C:\Program Files\Tablet\Wacom\32")
    while process.poll() is None:
        elapsed = time.time() - start
        stdout.write("\rUinsting. Elapsed time: %d seconds" % elapsed)
        stdout.flush()

    _result = True
    if process.returncode != 0:      # If call return is 0 (no errors) makes new reg entry for next script then restarts
        _result = False
        rc = process.returncode
    else:
        rc = process.returncode
    return rc, _result





# Experimenting with automated login
# user = getpass.getuser()
# print("The user name is %s" % user)
# user_name = os.getlogin()
# print("The user_name is %s" % user_name)
# user2 = os.environ.get("USERNAME")
# print(user2)
