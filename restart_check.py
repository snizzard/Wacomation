from wacfunc import ProcessTest, RegEntry, RebootSystem
from sys import stdout
import time
import datetime
from subprocess import Popen, call
script = "restart_check.py"
proc_list = ['Wacom_Tablet.exe', 'Wacom_TabletUser.exe',
             'Wacom_TouchUser.exe', 'WTabletServicePro.exe', 'WacomHost.exe']

for i in reversed(range(90)):
    stdout.write("\rCommence test in %i seconds" % i)
    stdout.flush()
    time.sleep(1)
stdout.write("\rWake Up Process Check")
_pass, _failure = ProcessTest('WAKEUP')
batch_path = r'C:\RestartLoop\resources\Restart_TabletDriverService.bat'
if not _pass:
    e_time = datetime.datetime.now()
    _date = e_time.strftime('%m-%d-%y')
    _time = e_time.strftime('%H:%M')
    with open(r"C:\RestartLoop\crash_log.txt", "a") as f:
        f.write("\nFailure occured: " + _date + " " + _time + "Failures:" + str(_failure))
        f.close()
    stdout.write("\rWake Test Failed. Restarting from sleep")
    call(batch_path, shell=True)
    Popen("rundll32.exe powrprof.dll,SetSuspendState Sleep")
else:
    i = 0
    while i < 5:
        driver_restart = call(batch_path, shell=True)
        _wait = i * 300
        time.sleep(_wait)
        stdout.write("\rProcess Check After %i Minutes" % (_wait / 60))
        _type = '%i MINUTE WAIT' % i
        _pass, _failure = ProcessTest(_type)
        if not _pass:
            e_time = datetime.datetime.now()
            _date = e_time.strftime('%m-%d-%y')
            _time = e_time.strftime('%H:%M')
            with open(r"C:\RestartLoop\crash_log.txt", "a") as f:
                f.write("\nDriver Restart Run %i: " + _date + " " + _time + "Failures:" + str(_failure) % i)
                f.close()
            stdout.write("\rFailure During %i Minutes Wait" % i)
            call(batch_path, shell=True)
        i += 1

RegEntry(script)
RebootSystem()
