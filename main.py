import sys
import cv2
import time
import socket
import numpy as np
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QCoreApplication
from PyQt5.Qt import QImage, QPixmap, QTimer, QThread

# Self-defined tracker
from centroid_tracker import *
# Self-defined constant
from common_define import *
# Self-defined widget
from calibration_widget import *

# Main window class
class main_window(QMainWindow):
    def __init__(self):
        super(main_window,self).__init__()
        loadUi('./ui/mainwindow.ui',self)

        # Shared variables
        self.image = None
        self.roi = (0,0,CAM_WIDTH,CAM_HEIGHT)
        self.pupil_max = 40
        self.cr_min = 230
        self.coeff = None
        self.cr_center = None
        self.pupil_center = None
        self.pcr_vec = None
        self.gaze_point = None
        self.data_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        # Controls of tracking
        self.do_tracking = False

        # Final data
        self.data_position = 0
        data = np.zeros((DATA_ROW_SIZE,5))
        self.final_data = [data]
        
        # Main window operations
        self.start_camera()
        self.tracker = centroid_tracker(self)
        self.cali_widget = calibration_widget(self)
        self.btnCalibration.clicked.connect(self.cali_widget.show)
        self.btnStart.clicked.connect(self.start_tracking)
        self.btnExit.clicked.connect(self.quit_app)
        self.btnSelROI.clicked.connect(self.select_roi)
        self.btnCamSetting.clicked.connect(self.camera_setting)
        
    # Capture via OpenCV API
    def start_camera(self):
        self.capture = cv2.VideoCapture(CAM_INDEX,cv2.CAP_DSHOW)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,CAM_WIDTH)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,CAM_HEIGHT)
        self.capture.set(cv2.CAP_PROP_FPS,CAM_FPS)
        # Capture image, may be used elsewhere
        self.image_thread = image_thread(self)
        self.image_thread.start()

        # Warm-up time
        time.sleep(1)
        # Tracker always online
        self.tracker_thread = track_thread(self)
        self.tracker_thread.start()
        # Preview on the main window
        self.timer_maindisplay = QTimer(self)
        self.timer_maindisplay.timeout.connect(self.main_preview)
        self.timer_maindisplay.start(8)

    def camera_setting(self):
        self.capture.set(cv2.CAP_PROP_SETTINGS,1)

    def select_roi(self):
        self.roi = (0,0,CAM_WIDTH,CAM_HEIGHT)
        time.sleep(0.05)
        self.roi = cv2.selectROI(windowName="Select ROI",img=self.image,showCrosshair=True,fromCenter=False)
        self.btnCalibration.setEnabled(True)

    def main_preview(self):
        # Main preview is set for monochrome only
        image = self.image.copy()
        if self.do_tracking:
            if not (np.isnan(self.pupil_center).any() or np.isnan(self.cr_center).any()):
                pupil = (int(self.pupil_center[0]),int(self.pupil_center[1]))
                cr = (int(self.cr_center[0]),int(self.cr_center[1]))
                cv2.line(image,pupil,cr,255,1,1)
            else:
                print("Target points missing!")
        qformat = QImage.Format_Indexed8
        out_image = QImage(image,
            image.shape[1],
            image.shape[0],
            image.strides[0],qformat)
        self.labMainPreview.setPixmap(QPixmap.fromImage(out_image))
        self.labMainPreview.setScaledContents(True)
    
    def start_tracking(self):
        self.do_tracking = True
        self.btnExit.setEnabled(True)
        if self.rad_net_ctrl.isChecked():
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
            s.bind(('127.0.0.1',NET_CONTROL_PORT))
            while True:
                data,addr = s.recvfrom(1024)
                if data == 'START':
                    break
        else:
            self.timer_data_recorder = QTimer(self)
            self.timer_data_recorder.timeout.connect(self.data_recorder)
            self.timer_data_recorder.start(1)
            self.timer_data_streamer = QTimer(self)
            self.timer_data_streamer.timeout.connect(self.data_streamer)
            self.timer_data_streamer.start(1)
        
    def data_streamer(self):
        data_string = "{}\t{}\t{}\t{}\n".format(self.gaze_point[0].item(),self.gaze_point[1].item(),\
                                                self.pcr_vec[0].item(),self.pcr_vec[1].item())                               
        self.data_socket.sendto(data_string.encode(encoding='ascii'),(NET_TARGET_ADDR,NET_TRANSFER_PORT))

    def data_recorder(self):
        if self.data_position == DATA_ROW_SIZE:
            data = np.zeros((DATA_ROW_SIZE,5))
            self.final_data.append(data)
            self.data_position = 0
        else:
            self.final_data[-1][self.data_position] = [time.time(),\
                                                        self.gaze_point[0].item(),self.gaze_point[1].item(),\
                                                        self.pcr_vec[0].item(),self.pcr_vec[1].item()]
            self.data_position += 1

    def quit_app(self):
        # Stop timer
        self.timer_data_recorder.stop()
        final_matrix = np.empty((0,5))
        for data in self.final_data:
            final_matrix = np.append(final_matrix,data,axis=0)
        timestamp = time.strftime("%Y%m%d-%H_%M_%S",time.localtime())
        filename = './data/'+timestamp+'.npz'
        np.savez_compressed(filename,final_matrix)
        QCoreApplication.instance().quit()

# Get image process
class image_thread(QThread):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
    
    def run(self):
        while True:
            image = self.parent.capture.read()[1]
            image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            x, y, w, h = self.parent.roi
            image = image[y:(y+h),x:(x+w)]
            self.parent.image = image

class track_thread(QThread):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
    
    def run(self):
        while True:
            self.parent.tracker.track()
'''
class record_thread(QThread):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent

    def run(self):
        while True:
            if self.parent.data_position == DATA_ROW_SIZE:
                data = np.zeros((DATA_ROW_SIZE,5))
                self.parent.final_data.append(data)
                self.parent.data_position = 0
            else:
                self.parent.final_data[-1][self.parent.data_position] = [time.time(),\
                                                        self.parent.gaze_point[0].item(),self.parent.gaze_point[1].item(),\
                                                        self.parent.pcr_vec[0].item(),self.parent.pcr_vec[1].item()]
                self.parent.data_position += 1
'''
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec_())