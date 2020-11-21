from PyQt5 import QtCore, QtWidgets
from Mw import Ui_Dialog
import MyThread

class Ui_MainWindow(Ui_Dialog):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.num = 0
        self.myThread = MyThread.MyThread()
        self.myThread.my_signal.connect(self.solt_set_text)
        self.myThread.quit_signal.connect(self.quitJob)

        self.filename = ""

    def setupUi(self, Dialog):
        super(Ui_MainWindow, self).setupUi(Dialog)
        self.issavenum.clicked.connect(self.myThread.setIsCloseWeber)
        self._dialog = Dialog
        desktop = QtWidgets.QApplication.desktop()
        x = (desktop.width() - Dialog.width()) // 2
        Dialog.move(x, 0)
        Dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.usernamestartrow.setValue(3)
        self.usernamestartcol.setValue(7)
        self.pswstartrow.setValue(3)
        self.pswstartcol.setValue(8)
        self.issavenum.setChecked(True)
        self.openfile.clicked.connect(self.openFile)
        self.startbutton.setEnabled(False)
        self.startbutton.clicked.connect(self.startJob)
        self.endbutton.setEnabled(False)
        self.endbutton.clicked.connect(self.quitJob)
        self.startorendlistener.setEnabled(False)
        self.startorendlistener.clicked.connect(self.nextJob)

    def solt_set_text(self, index, username, psw):
        self.num.setText(str(index))
        self.username.setText(username)
        self.psw.setText(psw)

    def openFile(self):
        self.filename = \
        QtWidgets.QFileDialog.getOpenFileName(None, 'OpenFile', r"C:\Users\wqk\Desktop", "账户密码xls (*.xls)")[0]
        self.filepath.setText(self.filename)
        self.startbutton.setEnabled(True)

    def startJob(self):
        self.myThread.setStartNum(self.startnum.value())
        self.myThread.setFileName(self.filename)
        self.myThread.setUsernameRC(self.usernamestartrow.value(), self.usernamestartcol.value())
        self.myThread.setPswRC(self.pswstartrow.value(), self.pswstartcol.value())
        self.myThread.setIsCloseWeber(self.issavenum.isChecked())
        self.myThread.start()
        self.startbutton.setEnabled(False)
        self.endbutton.setEnabled(True)
        self.startorendlistener.setEnabled(True)

    def quitJob(self):
        self.myThread.quit()
        self.startbutton.setEnabled(True)
        self.endbutton.setEnabled(False)
        self.startorendlistener.setEnabled(False)

    def nextJob(self):
        self.myThread.next_run()

    def retranslateUi(self, Dialog):
        super(Ui_MainWindow, self).retranslateUi(Dialog)
        _translate = QtCore.QCoreApplication.translate
        self._translate = _translate
