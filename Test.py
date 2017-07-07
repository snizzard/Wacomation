import sys, test_file, subprocess, wac_functions
from PyQt4 import QtGui, QtCore

global cycleType, cycleIterateNum, testRepeat, cycleProgNum, selectedTests
cycleType, cycleIterateNum, testRepeat, cycleProgNum, selectedTests = 'T', 3, 'R', 0, 'T'

selectedTests = ["Finst", "Check", "Oinst", "Check", "Uinst", "Check"]

# ------------------------------------------------------------- #
# Classes.                                                     #
# ----------------------------------------------------------- #
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(550, 530)
        self.setWindowTitle("WACOM   Installation Automation")
        self.setWindowIcon(QtGui.QIcon('Wacomlogo.ico'))
        self.main()


# ------------------------------------------------------------- #
# Main Window Radios, Buttons, and Textbox.                    #
# ----------------------------------------------------------- #
    def main(self):

        # Full radio.
        full = QtGui.QRadioButton('Full Test', self)
        full.move(25, 20)
        full.setChecked(True)

        # Fresh radio.
        fresh = QtGui.QRadioButton('Fresh Install', self)
        fresh.setFixedWidth(135)
        fresh.move(25, 50)

        # Process radio.
        procCheck = QtGui.QRadioButton('Process Check', self)
        procCheck.setFixedWidth(150)
        procCheck.move(25, 80)

        # Options button.
        options = QtGui.QPushButton("Options", self)
        options.clicked.connect(QtCore.QCoreApplication.instance().quit)
        options.move(415, 30)
        options.resize(110, 30)

        # Run button.
        run = QtGui.QPushButton("Run...", self)
        run.clicked.connect(self.runDialog)
        run.move(415, 80)
        run.resize(110, 30)

        # Output text box.
        outputBox = QtGui.QTextEdit(self)
        outputBox.setReadOnly(True)
        outputBox.move(15, 135)
        outputBox.resize(520, 380)

        self.show()

# ------------------------------------------------------------- #
# Run Dialog.                                                  #
# ----------------------------------------------------------- #
    def runDialog(self):

        # Dialog window.
        rd = QtGui.QDialog(self, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        rd.resize(305, 285)
        rd.setWindowTitle("Run...")
        rd.setModal(True)

        # Run variable "x" radio and input.
        rdrx = QtGui.QRadioButton("X:", rd)
        rdrx.move(50, 55)
        rdrxinp = QtGui.QPlainTextEdit(rd)
        rdrxinp.move(85, 52)
        rdrxinp.resize(50, 25)
        rdrxinp.setEnabled(False)

        def xInputToggle():
            if rdrx.isChecked():
                rdrxinp.setEnabled(True)
            else:
                rdrxinp.clear()
                rdrxinp.setEnabled(False)

        rdrx.toggled.connect(xInputToggle)

        # Run infinitely radio.
        rdrinf = QtGui.QRadioButton(u"\u221E", rd)
        rdrinf.move(50, 85)

        # Run timed radio and input.
        rdrtimed = QtGui.QRadioButton("Timed:", rd)
        rdrtimed.move(50, 115)
        rdrtinp = QtGui.QPlainTextEdit(rd)
        rdrtinp.move(107, 112)
        rdrtinp.resize(100, 25)
        rdrtinp.setEnabled(False)

        def timedInputToggle():
            if rdrtimed.isChecked():
                rdrtinp.setEnabled(True)
            else:
                rdrtinp.clear()
                rdrtinp.setEnabled(False)

        rdrtimed.toggled.connect(timedInputToggle)

        # Stop on err radio.
        rdrstop = QtGui.QRadioButton("Stop on err.", rd)
        rdrstop.move(50, 145)
        rdrstop.setChecked(True)

        # Disable repeat options if "Repeat" isn't selected.
        def repeatCheck():
            if rdrepeat.isChecked():
                rdrx.setEnabled(True)
                rdrinf.setEnabled(True)
                rdrtimed.setEnabled(True)
                rdrstop.setEnabled(True)
            else:
                rdrx.setEnabled(False)
                rdrinf.setEnabled(False)
                rdrtimed.setEnabled(False)
                rdrstop.setEnabled(False)

        # Repeat checkbox and enable/disable logic.
        rdrepeat = QtGui.QCheckBox("Repeat:", rd)
        rdrepeat.move(30, 25)
        rdrepeat.stateChanged.connect(repeatCheck)
        rdrepeat.setChecked(True)
        rdrepeat.setChecked(False)

        # Tweet checkbox.
        rdtweet = QtGui.QCheckBox("Tweet!", rd)
        rdtweet.move(30, 185)

        # Determine repeat type from radios above.
        def repeatType():
            global cycleType
            if rdrx.isChecked():
               cycleType = "Cycles"
            elif rdrinf.isChecked():
                cycleType = "Infinite"
            elif rdrtimed.isChecked():
                cycleType = "Hours"
            elif rdrstop.isChecked():
                cycleType = "Error"


        # Determine number of repeats for X and Timed tests.
        def repeatNumber():
            global cycleIterateNum
            if rdrx.isChecked():
                cycleIterateNum = rdrxinp.toPlainText()
            elif rdrtimed.isChecked():
                cycleIterateNum = rdrtinp.toPlainText()
            else:
                cycleIterateNum = "None"


        # Add test parameters to the meta.json file and start testing.
        def runClicked():


            if rdrepeat.isChecked():
                testRepeat = True   #  This needs to be adjusted to gather repeat details
                #test_file.type(repeatType)
                #test_file.number(repeatNumber)
            else:
                testRepeat = False
            test_file.MetaCreate(cycleType, cycleIterateNum, testRepeat)
           # execfile(r"C:\Wacomation\scripts\controller.py")

        # Run pushbutton.
        rdrun = QtGui.QPushButton("Run!", rd)
        rdrun.clicked.connect(runClicked)
        rdrun.resize(110, 30)
        rdrun.move(180, 240)


        # Shows the window.
        rd.show()



app = QtGui.QApplication(sys.argv)
GUI = MainWindow()
sys.exit(app.exec_())
