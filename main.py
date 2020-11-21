from MainWindow import Ui_MainWindow
from PyQt5 import QtWidgets,QtGui
import sys

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("wqk.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    widget.setWindowIcon(icon)
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())