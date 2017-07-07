from wac_functions import *
import json
from test_file import *
import platform

blist = ("False", "True")



new_test_file = NewFile()

test_system = platform.system()
print test_system
"""if test_system == 'Darwin':
        script = 'mac_script'
    elif test_system == 'Windows':
        script = 'win_script'
    else:
        script = 'Unsupported Operating System'
    next_test = getNextTest()
    if next_test == 'finst':
        test_result, test_error = InstallDriver()
    elif next_test == 'process check':
        test_error = ProcessTest(new_test_file)
    elif next_test == 'file check':
        #TODO
    elif next_test == 'registry check':
        test_error = RegistryValue()
    elif next_test == 'uinst':
        rc, test_error = UninstallDriver()

        #   timerStartTime = time.time()  # -- Timer for elapsed install time

  #  _os, _date, _time, driver, file_name, directory_name = CollectTestData()

# data = getMetaValue('newTest')
# if bool(blist.index(data)) == True:
 #   MetaCreate(0, 'cyles', 'False')"""
test_errors = FileTest(new_test_file)
print test_errors
raw_input('Enter')

"""_os, _date, _time, driver, file_name, dir_name = CollectTestData()  # These two lines are good
some_map = NewFile(driver, _os, _date, _time)                       # and can go in the GUI script at the end
map = ProcessTest(some_map)
print map
# print(_os + " " + _date + " " + _time + " " + file_name + " " + dir_name)

# MetaCreate(driver, _os, _date, _time, 1, "tests", "True")
testVal = getMetaValue("cycleNumber")
print testVal
setMetaValue("cycleNumber", 4)
testVal = getMetaValue("cycleNumber")
print testVal
RegEntry('controller.py')
RebootSystem()"""
