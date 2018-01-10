from chatting.changeui import *
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWidgets import QMessageBox
class Changefrontend(QtCore.QObject):
    changeinfo = QtCore.pyqtSignal(dict)
    def __init__(self,dicts):
        super(Changefrontend,self).__init__()
        self.ori = dicts
        self.window = QtWidgets.QDialog()
        self.window.setWindowFlags(Qt.Qt.MSWindowsFixedSizeDialogHint)
        self.gui = Ui_Change(self.window)
        self.gui.change.clicked.connect(self.collect)
        self.preset()
        self.window.show()
    def preset(self):
        self.gui.name.setText(self.ori['username'])
        self.gui.age.setText(str(self.ori['age']))
        self.gui.password1.setText(self.ori['password'])
        self.gui.address.setText(self.ori['address'])
    def collect(self):
        if self.gui.password1.text() != self.gui.password2.text():#对于密码的检查
            error = QMessageBox.warning(self.window, "Warning", "两次密码不相同!",QMessageBox.Yes)
        elif int(self.gui.age.text()) < 0 or int(self.gui.age.text()) >150:#对于年龄的检查
            error = QMessageBox.warning(self.window, "Warning", "年龄不符合规则!",QMessageBox.Yes)
        else:#将信息发送出去，及时的对chatting页面进行调整
            tmp = {"name":self.gui.name.text(),"password":self.gui.password1.text(),"age":self.gui.age.text(),"address":self.gui.address.text()}
            self.changeinfo.emit(tmp)
    def showChangeResult(self,command):
        if command == 1:
            sucess =QMessageBox.about(self.window,"Sucess!","您已修改成功！")
            self.window.close()
        elif command == 0:
            error = QMessageBox.warning(self.window, "Warning", "修改失败",QMessageBox.Yes)
        elif command == 2:
            error = QMessageBox.warning(self.window, "Warning", "该昵称已存在！",QMessageBox.Yes)
            self.gui.name.setText('')
