from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

from UI.setting_ui import *

from UI.capture_new_member import Capture_MainWindow
from UI.changepass import Changepass_MainWindow
from UI.remove import Remove_MainWindow

class Setting_MainWindow(QMainWindow):
    def __init__(self):
        # Init
        super().__init__()
        self.uic = Ui_Setting()
        self.uic.setupUi(self)

        self.uic.Button_add.clicked.connect(self.showCaptureWindow)
        self.uic.Button_remove.clicked.connect(self.showRemoveWindow)
        self.uic.Button_change.clicked.connect(self.showChangpassWindow)

        self.captureWindow = None
        self.changepassWindow = None
        self.removeWindow = None
    
    def showCaptureWindow(self):
        if self.captureWindow is None:
            self.captureWindow = Capture_MainWindow()
        self.captureWindow.show()
    
    def showRemoveWindow(self):
        if self.removeWindow is None:
            self.removeWindow = Remove_MainWindow()
        self.removeWindow.show()

    def showChangpassWindow(self):
        if self.changepassWindow is None:
            self.changepassWindow = Changepass_MainWindow()
        self.changepassWindow.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = Setting_MainWindow()
    main_win.show()
    sys.exit(app.exec())