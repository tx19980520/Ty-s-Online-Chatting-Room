import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from login.loginbackend import *
from login.loginfrontend import *
from login.login import *
from chatting.chatting import *
def main():
    app = QtWidgets.QApplication(sys.argv)
    program = Login()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
