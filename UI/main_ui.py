
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(820, 545)
        font = QtGui.QFont()
        font.setItalic(False)
        MainWindow.setFont(font)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(10, 10, 800, 361))

        self.label.setScaledContents(False)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.label.setStyleSheet("border: 2px solid black;")
        
        font = QtGui.QFont()
        font.setPointSize(18)
        
        self.line_Name = QtWidgets.QLineEdit(self.centralwidget)
        self.line_Name.setGeometry(QtCore.QRect(140, 470, 221, 40))
        self.line_Name.setFont(font)
        self.line_Name.setText("")
        self.line_Name.setObjectName("line_Name")

        self.line_time = QtWidgets.QLineEdit(self.centralwidget)
        self.line_time.setGeometry(QtCore.QRect(490, 470, 150, 40))
        self.line_time.setFont(font)
        self.line_time.setText("")
        self.line_time.setObjectName("line_time")

        self.line_date = QtWidgets.QLineEdit(self.centralwidget)
        self.line_date.setGeometry(QtCore.QRect(140, 410, 221, 40))
        self.line_date.setFont(font)
        self.line_date.setText("")
        self.line_date.setObjectName("line_date")
        
        self.line_state = QtWidgets.QLineEdit(self.centralwidget)
        self.line_state.setGeometry(QtCore.QRect(490, 410, 150, 40))
        self.line_state.setFont(font)
        self.line_state.setText("")
        self.line_state.setObjectName("line_state")

        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_name = QtWidgets.QLabel(self.centralwidget)
        self.label_name.setGeometry(QtCore.QRect(60, 470, 70, 35))
        self.label_name.setFont(font)
        self.label_name.setObjectName("label_name")
        
        self.label_time = QtWidgets.QLabel(self.centralwidget)
        self.label_time.setGeometry(QtCore.QRect(410, 470, 70, 35))
        self.label_time.setFont(font)
        self.label_time.setObjectName("label_time")
        
        self.label_state = QtWidgets.QLabel(self.centralwidget)
        self.label_state.setGeometry(QtCore.QRect(410, 410, 70, 35))
        self.label_state.setFont(font)
        self.label_state.setObjectName("label_state")

        self.label_date = QtWidgets.QLabel(self.centralwidget)
        self.label_date.setGeometry(QtCore.QRect(60, 410, 70, 35))
        self.label_date.setFont(font)
        self.label_date.setObjectName("label_date")

        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)

        self.Button_enalble = QtWidgets.QPushButton(self.centralwidget)
        self.Button_enalble.setGeometry(QtCore.QRect(680, 400, 130, 61))
        self.Button_enalble.setFont(font)
        self.Button_enalble.setObjectName("Button_enalble")


        self.Button_setting = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon("images/icon_setting.jpg")
        self.Button_setting.setIcon(icon)
        self.Button_setting.setIconSize(QtCore.QSize(50, 50))
        self.Button_setting.setGeometry(QtCore.QRect(730, 470, 50, 50))
        self.Button_setting.setFont(font)
        self.Button_setting.setObjectName("Button_setting")


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 840, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        MainWindow.setStyleSheet("""
            QLineEdit{
                background-color: #FFFFFF;
                border: 1px solid #C0C0C0;
                border-radius: 5px;
                color: rgb(0, 0, 0);
                background-color: rgb(255, 255, 255);
            }
            
            
            
            QLabel{
                color: #404040;
            }
            
            QPushButton{background-color: #00BFFF;color: #FFFFFF;border-radius: 15px;border: 2px solid #F0FFFF;}

            QPushButton:hover{background-color: #0077be;}
            
            QPushButton:pressed {background-color: #E9967A; color: #d6d6d6;}
            
        """)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_name.setText(_translate("MainWindow", "Name"))
        #self.Button_setting.setText(_translate("MainWindow", "SETTING"))
        self.label_time.setText(_translate("MainWindow", "Time"))
        self.Button_enalble.setText(_translate("MainWindow", "ENABLE"))
        self.label_state.setText(_translate("MainWindow", "State"))
        self.label_date.setText(_translate("MainWindow", "Date"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
