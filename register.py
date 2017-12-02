
from registerfrontend import *
from PyQt5 import QtCore

class Register(QtCore.QObject):
    registerRequest = QtCore.pyqtSignal(dict)
    def __init__(self,back):
        super(Register,self).__init__()
        self.ui = registerfrontend()
        self.back = back
        self.ui.register.connect(self.back.RegistertoServer)
        self.back.feedback.connect(self.ui.registerFeedback)
        self.ui.window.show()
