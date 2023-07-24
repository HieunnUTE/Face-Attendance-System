import sys
import cv2
import numpy as np
import os
import shutil
import re
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI.capture_new_member_ui import Ui_CaptureWindow
from ulti.format_face_detect_onnx import *


class Capture_MainWindow(QMainWindow):
    def __init__(self):
        # Init
        super().__init__()
        self.uic = Ui_CaptureWindow()
        self.uic.setupUi(self)

        # Chức năng của các nút nhấn
        self.uic.Button_start.clicked.connect(self.start_capture_video) # Nút start
        self.uic.Button_capture.clicked.connect(self.capture_img)   # Nút capture
        self.uic.Button_stop.clicked.connect(self.stop_capture_video)   # Nút stop
        
        self.thread = {}
    
    def closeEvent(self, event):
        """Hàm này sử dụng để stop các event (video frame) lại"""
        self.stop_capture_video()
    
    def stop_capture_video(self):
        """ Hàm này có nhiệm vụ xử lý --> ra các feature sau khi có được data (ảnh mới)"""
        try:
            # Thêm điều kiện để có thể tạo được feature mới
            if len(os.listdir(self.thread[1].saved_path)) >=3: 
                print("Added new member")
                
                # Tính trung bình feature
                feature = avg_emb(self.thread[1].saved_path)
                # Tạo 1 file text để lưu feature đó (type: np.array)
                file_name = self.name + ".txt"
                path_feature_file = os.path.join("Feature_member" ,file_name)
                f = open(path_feature_file, "w")
                f.write(re.sub("[^\S]+",",",np.array2string(feature).strip()))
            
            else:
                # Hiện thông báo nếu như không capture đủ điều kiện
                print("Not enought images")
            
            # Sau khi thực hiện các step trên thì sẽ xoá data (ảnh) --> tiết kiệm bộ nhớ
            # Chỉ giữ lại file text (file lưu feature)
            shutil.rmtree(self.thread[1].saved_path, ignore_errors=True)
            
            # Thực hiện dừng thread
            self.thread[1].stop()
        except: pass
        
        
    
    def start_capture_video(self):
        """Hàm có nhiệm vụ chạy webcam"""

        # Nhận tên input từ EditLine
        self.name = self.uic.lineNewname.text()
        
        # Thêm điều kiện xem tên có được nhập
        if self.name != '':
            # Nếu đã tồn tại tên <--> Có member mới
            path_name = "Data_member/" + self.name
            
            # Kiểm tra xem tên member mới này có tồn tại chưa
            if self.name + ".txt" not in os.listdir("Feature_member"):
                
                # Nếu chưa tồn tại thì sẽ tạo 1 folder để lưu data (ảnh face)
                os.mkdir(path_name)
                
                # Khởi tạo webcam: index là stt của camera, saved_path: đường dẫn ứng với tên member
                self.thread[1] = capture_video(index=0, saved_path = path_name)
                self.thread[1].start()
                self.thread[1].signal.connect(self.show_wedcam)
            
            # Nếu member đã tồn tại thì hiển thị thông báo
            else: print("Member's name exist")
        else: 
            print("Enter the new member's name")
        
    
    def capture_img(self):
        """Hàm sử dụng để capture khuôn mặt của member"""
        self.thread[1].capture()

    def show_wedcam(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.uic.label_addmember.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(800, 600, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

class capture_video(QThread):
    signal = pyqtSignal(np.ndarray)
    def __init__(self, index, saved_path):
        self.saved_path = saved_path
        self.cnt = 0
        self.index = index
        print("START WEBCAM")
        super(capture_video, self).__init__()

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, self.cv_img = cap.read()
            self.cv_img = cv2.flip(self.cv_img,1)
            org_img = self.cv_img.copy()
            if ret:
                image = trans_img(self.cv_img)
                confidences, boxes = ort_session.run(None, {input_name: image})
                boxes, _, _ = predict(self.cv_img.shape[1], self.cv_img.shape[0], confidences, boxes, threshold)
                for i in range(boxes.shape[0]):
                    box = boxes[i, :]
                    self.roi = org_img[box[1]:box[3],box[0]:box[2]]
                    cv2.rectangle(self.cv_img, (box[0], box[1]), (box[2], box[3]), (255,0,0), 3)

                self.signal.emit(self.cv_img)
    def stop(self):
        print("STOP WEBCAM")
        self.terminate()
    
    def capture(self):
        cv2.imwrite(f"{self.saved_path}/Img_{self.cnt}_webcam.jpg",self.roi)
        print(f"Img_{self.cnt}_webcam.jpg: Saved")
        self.cnt +=1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = Capture_MainWindow()
    main_win.show()
    sys.exit(app.exec())