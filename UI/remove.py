import os
import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from UI.remove_ui import Ui_Remove_MainWindow


class Remove_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_Remove_MainWindow()
        self.uic.setupUi(self)
        self.uic.button_remove.clicked.connect(self.remove_member)

    def remove_member(self):
        self.member_remove = self.uic.line_Remove.text()
        path = "Feature_member/"
        file_remove = [file_name for file_name in os.listdir(path) 
                        if file_name[:-4] == self.member_remove]
        
        if len(file_remove) == 1:
            file_path = path + file_remove[0]
            if os.path.isfile(file_path): 
                print("Member is removed")
                os.remove(file_path)
        else:
            print("Member is not exist")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = Remove_MainWindow()
    main_win.show()
    sys.exit(app.exec())