from changefrontend import *
from PyQt5 import QtCore
class Change(QtCore.QObject):
    def __init__(self,back):
        super(Change,self).__init__()
        self.back = back
        tmp = {}
        tmp['username'] = self.back.username
        tmp['age'] = self.back.age
        tmp['address'] = self.back.address
        tmp['password'] = self.back.password
        self.ui = changefrontend(tmp)
        self.ui.changeInfo.connect(self.back.userInfoChange)
        self.back.changeresult.connect(self.ui.showChangeResult)
