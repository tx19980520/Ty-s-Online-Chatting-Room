from registerui import Ui_Register
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWidgets import QMessageBox
class Registerfrontend(QtCore.QObject):
    register = QtCore.pyqtSignal(dict)
    def __init__(self):
        super(Registerfrontend,self).__init__()
        self.window =QtWidgets.QDialog()
        self.gui = Ui_Register(self.window)
        self.gui.start.clicked.connect(self.localCheck)
    def localCheck(self):
        if self.gui.password1.text() != self.gui.password2.text():
            error = QMessageBox.warning(self.window, "Warning", "两次密码不相同!",QMessageBox.Yes)
        elif int(self.gui.age.text()) < 0 or int(self.gui.age.text()) >150:
            error = QMessageBox.warning(self.window, "Warning", "年龄不符合规则!",QMessageBox.Yes)
        else:
            d = {}
            d['name'] = self.gui.name.text()
            d['password'] = self.gui.password1.text()
            d['address'] = self.gui.address.text()
            d['age'] = self.gui.age.text()
            self.register.emit(d)
    def registerFeedback(self,num):
        if num == 1:
            sucess =QMessageBox.about(self.window,"Sucess!","您已注册成功！")
            self.window.close()
        elif num == 2:
            self.gui.name.setText("")
            error = QMessageBox.warning(self.window, "Warning", "该昵称已被使用",QMessageBox.Yes)
