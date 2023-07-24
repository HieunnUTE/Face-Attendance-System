import sys
import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from UI.password_ui import Ui_Password_MainWindow
from UI.setting import Setting_MainWindow

class Password_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_Password_MainWindow()
        self.uic.setupUi(self)
        
        self.password = None
        self.settingWindow = None
        # self.uic.line_password.setEchoMode(QLineEdit.Password)
        self.uic.button_enter.clicked.connect(self.check_password)

    def check_password(self):
        self.password = self.uic.line_password.text()
        with open("password.txt","r") as f:
            true_pass = f.read()
            if self.password == true_pass:
                self.showSettingWindow()
            else:
                print("Wrong pass")
    
    def showSettingWindow(self):
        if self.settingWindow is None:
            self.settingWindow = Setting_MainWindow()
        self.settingWindow.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = Password_MainWindow()
    main_win.show()
    sys.exit(app.exec())