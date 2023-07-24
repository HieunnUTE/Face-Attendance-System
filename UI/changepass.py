import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from UI.changepass_ui import Ui_Changepass_Dialog

class Changepass_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_Changepass_Dialog()
        self.uic.setupUi(self)
        
        self.uic.button_ok.clicked.connect(self.change_password)

    def change_password(self):
        self.password = self.uic.line_old_pass.text()
        with open("password.txt","r") as f:
            true_pass = f.read()
            if self.password == true_pass:
                self.new_pass = self.uic.line_new_pass.text()
                if self.new_pass != '':
                    self.retype_pass = self.uic.line_retype_pass.text()
                elif self.new_pass == self.password:
                    print("Đây là pass cũ")
                
                if self.new_pass == self.retype_pass:
                    print("Password changed")
                    self.uic.line_old_pass.setText("")
                    self.uic.line_new_pass.setText("")
                    self.uic.line_retype_pass.setText("")
                    with open("password.txt","w") as f:
                        f.write(self.retype_pass)
                else:
                    self.uic.line_retype_pass.setText("")
                    print("Password dosent match")
            else:
                print("Wrong pass")
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = Changepass_MainWindow()
    main_win.show()
    sys.exit(app.exec())