import json
from platform import system, release
import datetime
import glob
import os

# Creates a new file for storing test results
def NewFile():  # Create new test file, driverName, os, date, time
    _os, _date, _time, driver, file_name, directory_name = CollectTestData()
    new_file = {"driver_name": driver, "os": _os, "run_date": _date, "run_time": _time, "tests": []}
    SaveFile(directory_name, file_name, new_file)
    return new_file

# Opens a saved file and adds a test to the test set
# contained in that file
def AddTest(_map, test_name, result, errors=None):  # dict=jsonMap, nameofTest, testResult
    if result:
        new = {'testName': test_name, "result": 'PASS'}
    else:
        new = {'testName': test_name, 'result': 'FAIL', 'report': errors}
    _map["tests"].append(new)
    return _map

# Saves test result file in specified directory
def SaveFile(_directory, file_name, jdata):
    if not os.path.isdir(r"C:\Wacomation\output\%s" % _directory):  # This block creates a directory hierarchy in the
        os.mkdir(r"C:\Wacomation\output\%s" % _directory)           # in the appropriate place if not there already
    file = r"C:\Wacomation\output\%s\%s.json" % (_directory, file_name)
    with open(file, "w") as f:
        json.dump(jdata, f, sort_keys=True, separators=(', ', ': '), indent=4)
    f.close()

# Loads a specified test file from specified directory
def LoadFile(_dir, file_name):
    file = r"C:\Wacomation\output\%s\%s.json" % (_dir, file_name)
    with open(file, 'r') as _file:
        load = json.load(_file)
    return load

# Modifies a specified key/value pair in the config file
def setMetaValue(keyName, newValue):
    path = r'C:\Wacomation\resources\tmp\config.json'
    with open(path, 'r') as f:
        meta_map = json.load(f)
    meta_map[keyName] = newValue
    f.close()
    with open(path, 'w') as f:
        json.dump(meta_map, f, sort_keys=True, separators=(', ', ': '), indent=4)
    f.close()

# Retrieves a value for specified key in config file
def getMetaValue(keyName):
    path = r'C:\Wacomation\resources\tmp\config.json'
    with open(path, 'r') as f:
        meta_map = json.load(f)
        keyValue = meta_map[keyName]
    f.close()
    return keyValue

def getNextTest():
    path = r'C:\Wacomation\resources\tmp\testSet.json'
    with open(path, 'r') as f:
        test_map = json.load(f)
        nt = "%i" % test_map["nextTest"]
        test_name = test_map["tests"][nt]
        f.close()
    return test_name

# Creates config file containing metadata for some test set
def MetaCreate(cycle_type, cycle_iterate, _repeat):                      # [driver, _os, start_date, start_time,] old params, may need later
    _os, start_date, start_time, driver, file_name, directory_name = CollectTestData()
    test_data = {'driverName': driver, 'os': _os, 'startDate': start_date, 'startTime': start_time,
                 'cycleNumber': 1, 'totalCycles': cycle_iterate, 'cycleType': cycle_type, 'repeat': _repeat}
    file = r"C:\Wacomation\resources\tmp\config.json"
    with open(file, "w") as f:
        json.dump(test_data, f, sort_keys=True, separators=(', ', ': '), indent=4)
    f.close()


# Still hasen't been used yet. I might change this to handle
# tmp directory containing metadata for current test instead of
# creating metadata for metadata.  Also considering converting this
# to a function that retrieves keynames from a JSON config file

# But we'll see now, won't we? Yes, we will indeed.
def ActiveTestData(selected_tests, last_test, current_cycle):
    active_data = {'selectedTests': selected_tests, 'lastTest': last_test, 'currentCycle': current_cycle}                  # I need to make this work for custom test runs, but for now I need to get it working
    file = r"C:\Wacomation\resources\active.json"                                                                          # for a full normal run
    with open(file, "w") as f:
        json.dump(active_data, f, sort_keys=True, separators=(', ', ': '), indent=4)
    f.close()

# I think this needs to be called within the MetaCreate function to make the process of
# creating a config file occur with fewer steps.
# Can also be used to create JSON config file.


def CollectTestData():  # perhaps a 'path' parameter pointing to driver location instead of hard-coded one
    for d in glob.glob(r"C:\Wacomation\driver\WacomTablet*.exe"):
        driver = d
        driver_name = os.path.splitext(d)[0]
    directory_name = driver_name[33:]
    file_name = "Run 1"
    start_time = datetime.datetime.now()
    _date = start_time.strftime("%m-%d-%y")
    _time = start_time.strftime("%H:%M")
    _os = system() + " " + release()
    return _os, _date, _time, driver, file_name, directory_name
