import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Changepass_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Changepass_MainWindow")
        Dialog.resize(529, 298)
        
        self.line_old_pass = QtWidgets.QLineEdit(Dialog)
        self.line_old_pass.setGeometry(QtCore.QRect(250, 40, 241, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.line_old_pass.setFont(font)
        self.line_old_pass.setObjectName("line_old_pass")

        self.label_current_pass = QtWidgets.QLabel(Dialog)
        self.label_current_pass.setGeometry(QtCore.QRect(30, 40, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_current_pass.setFont(font)
        self.label_current_pass.setObjectName("label_current_pass")

        self.label_create_pass = QtWidgets.QLabel(Dialog)
        self.label_create_pass.setGeometry(QtCore.QRect(30, 110, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_create_pass.setFont(font)
        self.label_create_pass.setObjectName("label_create_pass")

        self.line_new_pass = QtWidgets.QLineEdit(Dialog)
        
        self.line_new_pass.setGeometry(QtCore.QRect(250, 110, 241, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.line_new_pass.setFont(font)
        self.line_new_pass.setText("")
        self.line_new_pass.setObjectName("line_new_pass")

        self.label_retype_pass = QtWidgets.QLabel(Dialog)
        self.label_retype_pass.setGeometry(QtCore.QRect(30, 180, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_retype_pass.setFont(font)
        self.label_retype_pass.setObjectName("label_retype_pass")

        self.line_retype_pass = QtWidgets.QLineEdit(Dialog)
        self.line_retype_pass.setGeometry(QtCore.QRect(250, 180, 241, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.line_retype_pass.setFont(font)
        self.line_retype_pass.setText("")
        self.line_retype_pass.setObjectName("line_retype_pass")

        self.button_ok = QtWidgets.QPushButton(Dialog)
        self.button_ok.setGeometry(QtCore.QRect(400, 230, 93, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.button_ok.setFont(font)
        self.button_ok.setObjectName("button_ok")
        self.retranslateUi(Dialog)
        
        self.line_old_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_new_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_retype_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        
        Dialog.setStyleSheet("""
            QLineEdit{
                background-color: #FFFFFF;
                border: 1px solid #C0C0C0;
                border-radius: 5px;
            }
            
            QLineEdit:hover { background-color: #eee;}
            
            QLineEdit:pressed { background-color: #ccc; }
            
            QLabel{
                color: #404040;
            }
            
            
            QPushButton{
                background-color: #00BFFF;
                color: #FFFFFF;
                border-radius: 15px;
                border: 1px solid #00BFFF;
            }

            QPushButton:hover{
                background-color: #0077be;
                }
            
            QPushButton:pressed {
                background-color: #E9967A; color: #d6d6d6;
                }
        """)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Changepass_Dialog"))
        self.label_current_pass.setText(_translate("Dialog", "Mật khẩu hiện tại"))
        self.label_create_pass.setText(_translate("Dialog", "Tạo mật khẩu"))
        self.label_retype_pass.setText(_translate("Dialog", "Nhập lại mật khẩu mới"))
        self.button_ok.setText(_translate("Dialog", "OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Changepass_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
