
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Remove_MainWindow(object):
    def setupUi(self, Remove_MainWindow):
        Remove_MainWindow.setObjectName("Remove_MainWindow")
        Remove_MainWindow.resize(412, 160)
        self.centralwidget = QtWidgets.QWidget(Remove_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)

        self.label_Remove = QtWidgets.QLabel(self.centralwidget)
        self.label_Remove.setGeometry(QtCore.QRect(25, 75, 111, 21))
        self.label_Remove.setFont(font)
        self.label_Remove.setObjectName("label_Remove")
        
        font = QtGui.QFont()
        font.setPointSize(15)

        self.line_Remove = QtWidgets.QLineEdit(self.centralwidget)
        self.line_Remove.setGeometry(QtCore.QRect(130, 71, 151, 32))
        
        self.line_Remove.setFont(font)
        self.line_Remove.setObjectName("line_Remove")
        
        self.button_remove = QtWidgets.QPushButton(self.centralwidget) 
        self.button_remove.setGeometry(QtCore.QRect(290, 60, 110, 55))
        
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        
        self.button_remove.setFont(font)
        self.button_remove.setObjectName("button_remove")
        Remove_MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Remove_MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 412, 21))
        self.menubar.setObjectName("menubar")
        Remove_MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Remove_MainWindow)
        self.statusbar.setObjectName("statusbar")
        Remove_MainWindow.setStatusBar(self.statusbar)
        
        Remove_MainWindow.setStyleSheet("""
            QLineEdit{
                background-color: #FFFFFF;
                border: 1px solid #C0C0C0;
                border-radius: 8px;
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
        self.retranslateUi(Remove_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(Remove_MainWindow)

    def retranslateUi(self, Remove_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        Remove_MainWindow.setWindowTitle(_translate("Remove_MainWindow", "MainWindow"))
        self.label_Remove.setText(_translate("Remove_MainWindow", "Member"))
        self.button_remove.setText(_translate("Remove_MainWindow", "Remove"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Remove_MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Remove_MainWindow()
    ui.setupUi(Remove_MainWindow)
    Remove_MainWindow.show()
    sys.exit(app.exec_())
