import sys
import time
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog
from UI.main_ui import Ui_MainWindow
from ulti.format_face_detect_onnx import *
# from new_format_onnx import *
from UI.password import Password_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.passwordWindow = None
        self.thread = {}
        self.dict_store = {}

        self.uic.Button_enalble.clicked.connect(self.start_capture_video)
        self.uic.Button_setting.clicked.connect(self.showPasswordWindow)

    def start_capture_video(self):
        self.thread[1] = capture_video(index=0)
        try:
            self.thread[1].start()
            self.thread[1].signal.connect(self.show_webcam)
            self.thread[1].member = self.uic.line_Name
            self.thread[1].time = self.uic.line_time
            self.thread[1].state = self.uic.line_state
            self.thread[1].date = self.uic.line_date
            self.thread[1].dict_info = self.dict_store

        except: print("Lỗi ở hàm start capture")

    def show_webcam(self, cv_img):
        """Updates the image_label with a new opencv image"""
        if cv_img is not None:
            rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(821, 600, Qt.KeepAspectRatio)
            cv_imgPix = QPixmap.fromImage(p)
            self.uic.label.setPixmap(cv_imgPix)
        else: pass

    def showPasswordWindow(self):
        if self.passwordWindow is None:
            self.passwordWindow = Password_MainWindow()
        self.passwordWindow.show()
    


class capture_video(QThread):
    signal = pyqtSignal(np.ndarray)
    
    def __init__(self, index):
        self.index = index
        print("START WEBCAM")
        super(capture_video, self).__init__()
        self.check_member = {0:'Real',1:'Fake'}
    def run(self):
        cap = cv2.VideoCapture(self.index)
        enable = True
        time_enable = None

        year, month, day, time_check = map(int, time.strftime("%Y %m %d %S").split())
        date_attend = f"{year}/{month}/{day}"
        self.date.setText(date_attend)
        if time_check + 2 >= 60: time_check -= 60

        if 'Date' not in self.dict_info:
            self.dict_info.update({'Date':date_attend})
        else:
            if self.dict_info['Date'] != date_attend:
                self.dict_info = {}
        color = (255,0,0)
        self.img_process = None
        predicted = None
        while enable:
            ret, self.cv_img = cap.read()
            if ret:
                self.cv_img = cv2.flip(self.cv_img,1)
                hour, minn, sec = map(int, time.strftime("%H %M %S").split())
                
                if sec >= time_check + 10:
                    print("STOP WEBCAM")
                    enable = False
                    self.cv_img = cv2.imread("images/image_wait.jpg")

                if time_enable is not None:
                    if (hour,minn,sec) > time_enable:
                        self.member.setText("")
                        self.time.setText("")
                        self.state.setText("")
                        print("STOP WEBCAM")
                        enable = False
                        self.cv_img = cv2.imread("images/image_wait.jpg")
                
                if time_check + 2 <= sec:
                    org_img = self.cv_img.copy()
                    image = trans_img(self.cv_img)
                    confidences, boxes = ort_session.run(None, {input_name: image})
                    boxes, _, _ = predict(self.cv_img.shape[1], self.cv_img.shape[0], confidences, boxes, threshold)
                    time_attend = f"{hour}:{minn}:{sec}"


                    if boxes.shape[0] > 0:
                        box = boxes[0, :]
                        self.roi = org_img[box[1]:box[3],box[0]:box[2]]
                        if self.roi.shape >= (50, 50, 3) and self.img_process is None:
                            self.img_process = self.roi
                        
                        if self.img_process is not None:
                            with torch.no_grad():
                                img = processing_image(self.img_process)
                                output = model(img)[0]
                                _, predicted = torch.max(output, -1)
                        

                        if predicted == 1:
                            embedding_features = nor_emb(self.img_process)
                            normalized_features1 = feature_normalization(embedding_features) 
                            for file_name in os.listdir("Feature_member/"):
                                f = open("Feature_member/" + file_name, "r")
                                normalized_features2 = string2array64(f.read())
                                cosine = feature_comparison(normalized_features1, normalized_features2)
                                
                                if cosine > 0.7:
                                    name = str(file_name[:-4])
                                    string = f"{date_attend};{name};"
                                    thour,tmin,tsec = self.check(name,self.dict_info)
                                    if (thour,tmin,tsec) == (None,None,None) or (thour,tmin,tsec) <= (hour,minn,sec):
                                        allow_ = True                             
                                    else: allow_ = False
                                    
                                    if name not in self.dict_info:
                                        self.dict_info[f'{name}_state'] = 'Checkout'
                                    
                                    # CHECK - IN
                                    if self.dict_info[f'{name}_state'] == 'Checkout' and allow_:
                                        time_enable = hour,minn,sec+3
                                        self.dict_info.update({name:f"{hour}:{minn}:{sec}", f'{name}_state': 'Checkin'})
                                        self.member.setText(name)
                                        time.sleep(0.05)
                                        self.time.setText(f"{hour}:{minn}:{sec}")
                                        time.sleep(0.05)
                                        self.state.setText('Checkin')
                                        time.sleep(0.05)
                                        
                                        self.send_data_to_firebase(string + time_attend + ';' + 'Checkin')

                                    # CHECK - OUT
                                    elif self.dict_info[f'{name}_state'] == 'Checkin' and allow_:
                                        time_enable = hour,minn,sec+3
                                        self.dict_info.update({name:f"{hour}:{minn}:{sec}", f'{name}_state': 'Checkout'})
                                        
                                        self.member.setText(name)
                                        time.sleep(0.05)
                                        self.time.setText(f"{hour}:{minn}:{sec}")
                                        time.sleep(0.05)
                                        self.state.setText('Checkout')
                                        time.sleep(0.05)
                                        
                                        self.send_data_to_firebase(string + time_attend + ';' + 'Checkout')

                                    cv2.putText(self.cv_img,f"{name}", (box[0], box[1]-10),
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                                    
                        cv2.rectangle(self.cv_img, (box[0], box[1]), (box[2], box[3]), (0,255,0), 2)
                self.signal.emit(self.cv_img)
                
    def stop(self):
        print("STOP WEBCAM")
        self.terminate()

    def check(self,name,dict_info):
        if name in dict_info:
            time_ = dict_info[name]
            time_list = time_.split(":")
            thour,tmin,tsec = int(time_list[0]),int(time_list[1]),int(time_list[2]) + 40
            return thour,tmin,tsec
        else: return None,None,None
    
    def send_data_to_firebase(self,line_send):
        data = {}
        name = None
        date = None
        line_data = line_send.strip().split(";")
        if date is None:
            date = line_data[0]
            name = line_data[1]
            data[line_data[3].lower()] = line_data[2]
        elif line_data[0] == date and line_data[1] == name:
            data[line_data[3].lower()] = line_data[2]
        else:
            db.reference("Sophic_Attendance").child(date).child(name).update(data)
            date = line_data[0]
            name = line_data[1]
            data = {}
            data[line_data[3].lower()] = line_data[2]
        db.reference("Sophic_Attendance").child(date).child(name).update(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())