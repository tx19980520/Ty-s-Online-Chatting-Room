from changeui import *
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWidgets import QMessageBox
class changefrontend(QtCore.QObject):
    changeInfo = QtCore.pyqtSignal(dict)
    def __init__(self,dicts):
        super(changefrontend,self).__init__()
        self.ori = dicts
        self.window = QtWidgets.QDialog()
        self.gui = Ui_Change(self.window)
        self.gui.change.clicked.connect(self.collect)
        self.preset()
        self.window.show()
    def preset(self):
        self.gui.name.setText(self.ori['username'])
        self.gui.age.setText(str(self.ori['age']))
        self.gui.password1.setText(self.ori['password'])
        self.gui.address.steText(self.ori['address'])
    def collect(self):
        if self.gui.password1.text() != self.gui.password2.text():
            error = QMessageBox.warning(self.window, "Warning", "两次密码不相同!",QMessageBox.Yes)
        elif int(self.gui.age.text()) < 0 or int(self.gui.age.text()) >150:
            error = QMessageBox.warning(self.window, "Warning", "年龄不符合规则!",QMessageBox.Yes)
        else:
            tmp = {"name":self.gui.name.text(),"password":self.gui.password1.text(),"age":self.gui.age.text(),"address":self.gui.address.text()}
            self.changeInfo.emit(tmp)
    def showChangeResult(self,command):
        if command == 1:
            sucess =QMessageBox.about(self.window,"Sucess!","您已注册成功！")
        elif command == 0:
            error = QMessageBox.warning(self.window, "Warning", "修改失败",QMessageBox.Yes)
