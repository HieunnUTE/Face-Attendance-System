from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_Setting(object):
    def setupUi(self, Setting):
        Setting.setObjectName("Setting")
        Setting.resize(521, 200)
        
        # set the window background color
        Setting.setStyleSheet("background-color: rgb(240, 240, 240);")
        
        self.Button_change = QtWidgets.QPushButton(Setting)
        self.Button_change.setGeometry(QtCore.QRect(155, 40, 221, 51))
        self.Button_change.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Button_change.setFont(font)
        self.Button_change.setObjectName("Button_change")
        
        self.Button_add = QtWidgets.QPushButton(Setting)
        self.Button_add.setGeometry(QtCore.QRect(30, 110, 221, 51))
        self.Button_add.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Button_add.setFont(font)
        self.Button_add.setObjectName("Button_add")
        
        self.Button_remove = QtWidgets.QPushButton(Setting)
        self.Button_remove.setGeometry(QtCore.QRect(270, 110, 221, 51))
        self.Button_remove.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Button_remove.setFont(font)
        self.Button_remove.setObjectName("Button_remove")

        self.Button_change.setStyleSheet("QPushButton{border-radius: 25px; background-color: #1E90FF; color: white;}"
                                  "QPushButton:hover{background-color: #0077be;}")
        self.Button_add.setStyleSheet("QPushButton {border-radius: 25px; background-color: #228B22; color: white;}"
                                    "QPushButton:hover{background-color: #00C957;}")
        self.Button_remove.setStyleSheet("QPushButton {border-radius: 25px; background-color: #DC143C; color: white;}"
                                        "QPushButton:hover {background-color: #FF4500;}")

        self.retranslateUi(Setting)
        QtCore.QMetaObject.connectSlotsByName(Setting)

    def retranslateUi(self, Setting):
        _translate = QtCore.QCoreApplication.translate
        Setting.setWindowTitle(_translate("Setting", "Dialog"))
        self.Button_change.setText(_translate("Setting", "Change password"))
        self.Button_add.setText(_translate("Setting", "Add member"))
        self.Button_remove.setText(_translate("Setting", "Remove member"))


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    Setting = QtWidgets.QDialog()
    ui = Ui_Setting()
    ui.setupUi(Setting)
    Setting.show()
    sys.exit(app.exec_())
